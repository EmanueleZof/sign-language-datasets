import tensorflow_datasets as tfds

# noinspection PyUnresolvedReferences
from pose_format import PoseHeader, Pose
from pose_format.numpy import NumPyPoseBody
from pose_format.utils.reader import BufferReader

from sign_language_datasets.datasets.signsuisse.signsuisse import _POSE_HEADERS
from sign_language_datasets.datasets.config import SignDatasetConfig


def load_pose(pose_header, tf_pose):
    fps = int(tf_pose["fps"].numpy())
    pose_body = NumPyPoseBody(fps, tf_pose["data"].numpy(), tf_pose["conf"].numpy())
    return Pose(pose_header, pose_body)


config = SignDatasetConfig(name="example", version="1.0.0",
                           include_video=True,
                           include_pose="holistic",
                           process_video=False,
                           sample_size=10)
dataset = tfds.load(name='sign_suisse', builder_kwargs={"config": config})

# pylint: disable=protected-access
with open(_POSE_HEADERS[config.include_pose], "rb") as buffer:
    pose_header = PoseHeader.read(BufferReader(buffer.read()))

for datum in dataset["train"]:
    print("Concept: ", datum['name'].numpy().decode('utf-8'))
    print("category: ", datum['category'].numpy().decode('utf-8'))
    print("Video: ", datum['video'].numpy().decode('utf-8'))
    print("Pose path: ", datum['pose']['path'].numpy().decode('utf-8'))
    print("Pose: ", load_pose(pose_header, datum['pose']))
    print("---")
    print("Example: ", datum['exampleText'].numpy().decode('utf-8'))
    print("Example Video: ", datum['exampleVideo'].numpy().decode('utf-8'))
    print("Example Pose path: ", datum['examplePose']['path'].numpy().decode('utf-8'))
    print("Example Pose: ", load_pose(pose_header, datum['examplePose']))
    print("---")
    print('\n\n')
# from pose_format import Pose
#
# with open(
#         "/home/nlp/amit/tensorflow_datasets/downloads/extracted/TAR_GZ.nlp.biu.ac.il_amit_data_pose_holi_signZjjPSbhafIJNhjgLBLdTYBNZG-89WSEmWE4dJsKvLBM.tar.gz/signsuisse/ss8f848ef2e416a402399a7dcec0b83838.pose",
#         "rb") as f:
#     pose = Pose.read(f.read())
#
# print("total points", sum(len(c.points) for c in pose.header.components))
#
# with open("/home/nlp/amit/sign-language/sign-language-datasets/sign_language_datasets/datasets/signsuisse/holistic.poseheader", "wb") as f:
#     pose.header.write(f)
