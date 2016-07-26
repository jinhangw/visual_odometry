"""

MIT License (MIT)

Copyright (c) SUMMER 2016, Carnegie Mellon University

Author: Jahdiel Alvarez

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


"""

from Common_Modules import *

class CameraParams:
    """ A class for the parsing of the Camera Parameter's text file.
    The parameters obtained are used for the py-MVO algorithm."""
    def __init__(self, txt_file):
        """

        Attributes:

        self.folder               Image Sequence's Directory
        self.format               Images' File Format (e.g. PNG, JPG)
        self.isProjMat            Boolean: is True if the Projection Matrix is used
        self.ProjMat              Camera Projection Matrix
        self.CamIntrinMat         Camera Intrinsic Matrix
        self.featureDetector      Feature Detector: SIFT, FAST, SURF, SHI-TOMASI
        self.GPS_FLAG             GPS Flag: Look at the CameraParams.txt file to see the GPS_FLAGS
        self.groundTruth          Ground Truth Poses: a text file with the transformation matrices as 1-D arrays(KITTI dataset format)

        See the CameraParams text file to see an in depth explanation of each attribute.

        """

        # Read the Camera Params file
        with open(txt_file) as f:
            self.txt = f.readlines()
        idx = 46  # The index where the attributes begin
        self.folder = self.txt[idx].strip()
        self.format = self.txt[idx+1].strip()
        self.isProjMat = self.txt[idx+2].strip()

        if self.isProjMat == 'True' or self.isProjMat == 'TRUE':
            # Convert to a 1-D float list
            self.ProjMat = [float(i.strip()) for i in self.txt[idx+3].split()]
            # Convert to a 3x4 numpy array
            self.ProjMat = np.array([[self.ProjMat[0], self.ProjMat[1], self.ProjMat[2], self.ProjMat[3]],
                                     [self.ProjMat[4], self.ProjMat[5], self.ProjMat[6],self.ProjMat[7]],
                                     [self.ProjMat[8], self.ProjMat[9], self.ProjMat[10], self.ProjMat[11]]])

            self.CamIntrinMat = None

        else:
            # Convert to a 1-D float list
            self.CamIntrinMat = [float(i.strip()) for i in self.txt[idx+4].split()]
            # Convert to a 3x3 numpy array
            self.CamIntrinMat = np.array([[self.CamIntrinMat[0], self.CamIntrinMat[1], self.CamIntrinMat[2]],
                                          [self.CamIntrinMat[3], self.CamIntrinMat[4], self.CamIntrinMat[5]],
                                          [self.CamIntrinMat[6], self.CamIntrinMat[7], self.CamIntrinMat[8]]])
            self.ProjMat = None

        # If Projection Matrix used, decompose to obtain the Camera Intrinsic Matrix
        if isinstance(self.CamIntrinMat, np.ndarray) is False:
            self.decomposedP = np.array(cv2.decomposeProjectionMatrix(self.ProjMat))
            self.CamIntrinMat = self.decomposedP[0].reshape((3, 3))

        self.featureDetector = self.txt[idx+5].strip()
        self.GPS_FLAG = self.txt[idx+6].strip()
        self.groundTruth = self.txt[idx+7].strip()
        # If groundTruth is not provided, it is assigned as False
        if self.groundTruth == '' or self.groundTruth == 'None':
            self.groundTruth = False


