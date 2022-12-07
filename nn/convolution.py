import math

import numpy as np
from numba import njit


def convolve(tensor, kernels, stride, dilation, full=False):
    kernel_size = np.array(kernels.shape[1:-1])
    output_slice_size = get_convolution_output_size(tensor.shape[:-1], kernel_size, stride, dilation, full)

    sections = get_convolution_sections(tensor, kernel_size, stride, dilation, full)
    flatten_kernels = kernels.copy().reshape((len(kernels), -1))
    flatten_convoluted = sections @ flatten_kernels.T
    convoluted = flatten_convoluted.reshape((output_slice_size[0], output_slice_size[1], len(kernels)))
    return convoluted


@njit
def get_convolution_sections(data, kernel_size, stride, dilation, full):
    dilated_kernel_size = get_dilated_kernel_size(kernel_size, dilation)
    output_slice_size = get_convolution_output_size(data.shape[:-1], kernel_size, stride, dilation, full)

    sections_count = np.prod(output_slice_size)
    kernel_length = np.prod(kernel_size)
    sections = np.zeros((sections_count, kernel_length * data.shape[-1]))

    offset = -dilated_kernel_size+1 if full else np.array([0, 0])

    anchors0 = [i * stride[0] + offset[0] for i in range(output_slice_size[0])]
    anchors1 = [i * stride[1] + offset[1] for i in range(output_slice_size[1])]

    linear_index = 0
    for center0 in anchors0:
        for center1 in anchors1:
            sections[linear_index] = get_single_convolution_section(data, (center0, center1), kernel_size, dilation)
            linear_index += 1

    return sections


@njit
def get_single_convolution_section(data, pos, kernel_size, dilation):
    section = np.zeros((np.prod(kernel_size), data.shape[-1]))

    positions0 = [pos[0] + dilation[0] * i for i in range(kernel_size[0])]
    positions1 = [pos[1] + dilation[1] * i for i in range(kernel_size[1])]

    linear_index = 0
    for pos0 in positions0:
        for pos1 in positions1:
            index_valid = 0 <= pos0 < data.shape[0] and 0 <= pos1 < data.shape[1]
            section[linear_index] = data[pos0, pos1, :] if index_valid else np.zeros((data.shape[-1],))
            linear_index += 1

    return section.flatten()


@njit
def get_convolution_output_size(data_size, kernel_size, stride, dilation, full=False):
    data_size = np.array(data_size)
    dilated_kernel_size = get_dilated_kernel_size(kernel_size, dilation)

    available_space = (data_size - dilated_kernel_size) + 1
    if full:
        available_space += 2 * kernel_size - 2

    size_float = available_space / stride
    size = np.array([math.ceil(size_float[0]), math.ceil(size_float[1])])
    return size


@njit
def get_dilated_kernel_size(kernel_size, dilation):
    return (kernel_size - 1) * dilation + 1
