
import matplotlib.pyplot as plt

def get_stack_keys(data, num_stacks=5):
    """Creates a list containing the values where we will build our stacks.
    Returns an evenly-spaced list of real values of length num_stacks between
    lower_bound and upper_bound (the minimum and maximum values  in data,
    respectively).
    Because we want to include the upper_bound, we need to space the remaining
    values range / (num_stacks - 1) units apart from each other.
    ================================================================================
    Parameters
    ----------
        data (list-like):
            A list of real numbers. This is the raw data we are exploring.
        num_stacks (int):
            The number of stacks we want to build on our dotplot. Must be a whole
            number greater than 1. Default value is 5.
    Returns
    -------
    A list of real values where we want to place our stacks.
    ================================================================================
    """
    upper_bound = max(data)
    lower_bound = min(data)
    stack_keys = [lower_bound + i * (upper_bound - lower_bound) / (num_stacks-1)
              for i in range(num_stacks)]
    return stack_keys

def get_stack_dict(data, num_stacks=5, keys=None):
    """Assigns each observation to the appropriate stack.
    Creates a dictionary of lists, where each key is a stack_key, then
    adds observations to the list corresponding to the correct stack.
    ================================================================================
    Parameters
    ----------
        data (list-like):
            A list of real numbers. This is the raw data we are exploring.
        num_stacks (int):
            The number of stacks we want to build on our dotplot. Must be a whole
            number greater than 1. Default value is 5.
        keys (list-like):
            Particular values to use for the keys. This can create more attractive
            dotplots, but depends on the user including evenly-spaced keys.
    Returns
    -------
    A dictionary, where the keys are stack_keys, and the value corresopnding to
    each key is a list of observations that fall on that stack.
    ================================================================================
    """
    if keys == None:
        keys = get_stack_keys(data=data, num_stacks=num_stacks)
    stack_dict = {key:[] for key in keys}

    for observation in data:
        # a flag variable, indicating we need to add our value to the final
        # stack. by default, we assume we'll have to do this.
        add_to_end = True

        # step through the list, when observation is between two entries, add
        # it to the list corresponding to the key on the left. since we're
        # comparing two adjacent list entries, we'll need to iterate over the
        # index.
        for i in range(1, len(keys)):
            # if the observation is between these two keys
            if keys[i-1] <= observation < keys[i]:
                # add it to the lower key's list of values
                stack_dict[keys[i-1]].append(observation)

                # we don't need to add it to the end of the list
                add_to_end = False

                # we don't need to continue looking for the right key
                break

        # if we make it to the end of the list without finding the key to the
        # left of the value of the observation, that means we need to add it
        # to the final stack
        if add_to_end:
            stack_dict[keys[-1]].append(observation)

    return stack_dict

def get_points(stack_dict):
    """Generates a list of points for the scatterplot based on the stack_dict.
    Iterates over the keys in stack_dict, and creates a list of points whose
    x-values are the keys, and whose y-values allow the points to stack over the
    desired x-value.
    ================================================================================
    Parameters
    ----------
        stack_dict (dict):
            a dictionary whose keys are the desired x-values for the dotplot,
            and whose values are the number of observations falling on that stack.
    Returns
    -------
    A list of ordered pairs, representing points for the scatterplot to mimic a
    dotplot.
    ================================================================================
    """

    # the list to hold the points
    ordered_pairs = []

    # iterate over the items in the list
    for key, observations in stack_dict.items():

        # add a point onto the stack for each value in this list
        for i, obs in enumerate(observations):
            ordered_pairs.append((key, i+1))

    return ordered_pairs

import matplotlib.pyplot as plt

def dotplot(data, num_stacks=5, keys=None, rotation=None, title=None,
            xlabel=None, ylabel=None, filename='image.png',  show=False):
    """Function to create the dotplot and save it to a file.
    This function provides a minimal interface for creating a dotplot with
    matplotlib. The smallest amount of information necessary to create the dotplot
    is a list of raw values for the data variable. For example:
        observations = [1,2,3,3,3,3,5,6,6,2,3,4,2,1,2]
        dotplot(data=observations)
    By default, this will create five stacks in the dotplot and save the file
    under the name 'image.png' in the working directory.
    ================================================================================
    Parameters
    ----------
        data (list-like):
            The list of observations (real numbers) to be plotted.
        num_stacks (int):
            The number of stacks to create in the dot plot.
            Default: 5
        keys (list):
            A list of real numbers indicating the specific locations for stacks on
            the x-axis.
            Default: None
        rotation (int):
            Degrees to rotate the labels on the x-axis. 45 is a good value if
            the keys are decimals longer than 3 places and you want to prevent
            them from overlapping.
            Default: None
        title (str):
            Title of the plot
            Default: None 
        xlabel (str):
            Label to be applied to the x-axis
            Default: None
        ylabel (str):
            Label to be applied to the y-axis
            Default: None
        filename (str):
            The name of the image.
            Default: 'image.png'
        show (bool):
            Whether or not to call plt.show(). If in a notebook, set show=True
            to show the dotplot inline.
            Default: False
    Returns
    -------
    None
    ================================================================================
    """

    # create the stack_dict
    stack_dict = get_stack_dict(data, num_stacks, keys)

    # get the keys (will return a list containing the same values if keys=None)
    keys = list(stack_dict.keys())

    # get the list of points
    points = get_points(stack_dict)

    # split the ordered pairs into x-values and y-values to make matplotlib happy
    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    # create the figure
    plt.figure(figsize=(15,7))

    # plot the scatterplot
    plt.scatter(xs, ys, s=4000/len(keys))

    # in order to view the ylabel, leave y-axis visible just make yticks empty
    if ylabel:
        plt.yticks([])
    else:
        plt.gca().get_yaxis().set_visible(False)

    # set the x-ticks
    plt.xticks(list(stack_dict.keys()), fontsize=200/num_stacks, rotation=rotation)

    # set the vertical limits
    plt.ylim(0, 1.1 * max(ys))

    # hide the box around the axis
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    # add plot title, if specified
    if title:
        plt.title(title, fontsize=220/num_stacks)

    # add axis labels, if specified
    if xlabel:
        plt.xlabel(xlabel, fontsize=180/num_stacks)
    if ylabel:
        plt.ylabel(ylabel, fontsize=180/num_stacks)

    # save the file
    plt.savefig(filename)

    # show the figure, if possible
    if show:
        plt.show()