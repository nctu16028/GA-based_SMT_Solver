#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "utils.h"

namespace py = pybind11;

// Wrapper function to handle NumPy arrays in Python
int prim_toBind(int scalar, py::array_t<int> array) {
    // Accessing the NumPy array
    py::buffer_info buf_info = array.request();
    int* ptr = static_cast<int*>(buf_info.ptr);

    // Create a vector from the NumPy array data
    std::vector<int> cpp_array(ptr, ptr + buf_info.size);

    // Call the original C++ function
    return prim(scalar, cpp_array);
}

PYBIND11_MODULE(utils, m) {
    m.def("prim", &prim_toBind);
}
