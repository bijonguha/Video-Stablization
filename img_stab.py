# Installed package
import numpy as np
import cv2
from vidgear.gears import VideoGear


def stablize_video(path = 'video.mp4'):
    '''
    Function for stablizing Videos

    path : str
        Path of the video file

    Returns
        None

    '''
    # open any valid video stream with stabilization enabled(`stabilize = True`)
    stream_stab = VideoGear(source=path, stabilize=True, **{"SMOOTHING_RADIUS":50, "BORDER_TYPE":"replicate"}).start()

    # open same stream without stabilization for comparison
    stream_org = VideoGear(source=path).start()

    # loop over
    while True:

        # read stabilized frames
        frame_stab = stream_stab.read()

        # check for stabilized frame if Nonetype
        if frame_stab is None:
            break

        # read un-stabilized frame
        frame_org = stream_org.read()

        # concatenate both frames
        output_frame = np.concatenate((frame_org, frame_stab), axis=1)

        # put text over concatenated frame
        cv2.putText(
            output_frame,
            "Before",
            (10, output_frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )
        cv2.putText(
            output_frame,
            "After",
            (output_frame.shape[1] // 2 + 10, output_frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )
        
        output_frame = cv2.resize(output_frame, (0, 0), fx = 0.3, fy = 0.3)
        # Show output window
        cv2.imshow("Stabilized Frame", output_frame)

        # check for 'q' key if pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # close output window
    cv2.destroyAllWindows()

    # safely close both video streams
    stream_org.stop()
    stream_stab.stop()

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='FcarScan Task - Video stabilization')

  parser.add_argument('--path', default='video.mp4', type=str, help='Path of the Video file')

  args = parser.parse_args()

  stablize_video(path = args.path)