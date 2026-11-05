# WITHDRAWN — do not install face candidate19018

The first face-only candidate uploaded in this thread is withdrawn. This is not a warning about the original FULL8 RC7; retain the user's working RC7.

An independent index-buffer check found that the candidate's inherited LOD builder incorrectly treated the entire reserved index buffer as drawn geometry. The original mesh has skin and hair sections with separate BaseIndex offsets. The low LOD then contained out-of-range indices. Earlier checks of RequiredBones, serialized lengths and source weights did not detect this. A build succeeding did not establish a valid render asset.

The next face build must copy each section's actual drawn triangles by BaseIndex/NumTriangles, exclude padding from the draw calls, and validate every index against the actual vertex count in BOTH LODs of all24assets. Source/repair-full8-rc10-face-detail adds that check and keeps the RC7 neck geometry and original source-calibrated oral weights.

Old Drive patch id:1ffS2H9r2rskhG-pJOViILFRctF8Q3y-4 has been renamed WITHDRAWN-DO-NOT-INSTALL. Old GitHub artifacts from the first two face workflows are not recommended for installation. No device verification has been performed.

UCL remains unfinished. There is no integrated native UCL mode in the withdrawn face candidate or in a face-only replacement.
