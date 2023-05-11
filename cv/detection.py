import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# # For static images:
# IMAGE_FILES = []
# BG_COLOR = (192, 192, 192) # gray
# with mp_pose.Pose(
#     static_image_mode=True,
#     model_complexity=2,
#     enable_segmentation=True,
#     min_detection_confidence=0.5) as pose:
#   for idx, file in enumerate(IMAGE_FILES):
#     image = cv2.imread(file)
#     image_height, image_width, _ = image.shape
#     # Convert the BGR image to RGB before processing.
#     results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     if not results.pose_landmarks:
#       continue
#     print(
#         f'Nose coordinates: ('
#         f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
#         f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
#     )

#     annotated_image = image.copy()
#     # Draw segmentation on the image.
#     # To improve segmentation around boundaries, consider applying a joint
#     # bilateral filter to "results.segmentation_mask" with "image".
#     condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
#     bg_image = np.zeros(image.shape, dtype=np.uint8)
#     bg_image[:] = BG_COLOR
#     annotated_image = np.where(condition, annotated_image, bg_image)
#     # Draw pose landmarks on the image.
#     mp_drawing.draw_landmarks(
#         annotated_image,
#         results.pose_landmarks,
#         mp_pose.POSE_CONNECTIONS,
#         landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#     cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
#     # Plot pose world landmarks.
#     mp_drawing.plot_landmarks(
#         results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

# For webcam input:
def human_detection():
  cap = cv2.VideoCapture(8)
  with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    counter=0

    Left_Shoulder_x_List=[]
    Right_Shoulder_x_List=[]
    Left_Hip_x_List=[]
    Right_Hip_x_List=[]

    Left_Shoulder_y_List=[]
    Right_Shoulder_y_List=[]
    Left_Hip_y_List=[]
    Right_Hip_y_List=[]

    while cap.isOpened():
      success, image = cap.read()

      # begin_instruct = input('Please type True when you hope begin Massage')
      # if ( begin_instruct != 'True'):
      #   continue
      
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = pose.process(image)
      cv2.imshow('MassageMate Vision Interface', image)
      
      if not results.pose_landmarks:
        continue

      # print(
      #     f'Left Shoulder coordinates: ('
      #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width}, '
      #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height})'
      # )

      Left_Shoulder_x_List.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x)
      Left_Shoulder_y_List.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y)

      # print(
      #     f'Right Shoulder coordinates: ('
      #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width}, '
      #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height})'
      # )

      Right_Shoulder_x_List.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x)
      Right_Shoulder_y_List.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y)

      # print(
      #     f'Left Hip coordinates: ('
      #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * image_width}, '
      #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * image_height})'
      # )

      Left_Hip_x_List.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x)
      Left_Hip_y_List.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y)

      # print(
      #     f'Right Hip coordinates: ('
      #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * image_width}, '
      #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height})'
      # )

      Right_Hip_x_List.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x)
      Right_Hip_y_List.append(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y)

      counter+=1
      print(counter)

      if cv2.waitKey(5) & 0xFF == 27:
        break

      if counter == 20:

        Left_Shoulder_x=sum(Left_Shoulder_x_List)/len(Left_Shoulder_x_List)
        Left_Shoulder_y=sum(Left_Shoulder_y_List)/len(Left_Shoulder_y_List)
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x = Left_Shoulder_x
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y = Left_Shoulder_y   

        Right_Shoulder_x=sum(Right_Shoulder_x_List)/len(Right_Shoulder_x_List)
        Right_Shoulder_y=sum(Right_Shoulder_y_List)/len(Right_Shoulder_y_List)
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x = Right_Shoulder_x
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y = Right_Shoulder_y  

        Left_Hip_x=sum(Left_Hip_x_List)/len(Left_Hip_x_List)
        Left_Hip_y=sum(Left_Hip_y_List)/len(Left_Hip_y_List)
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x = Left_Hip_x
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y = Left_Hip_y  

        Right_Hip_x=sum(Right_Hip_x_List)/len(Right_Hip_x_List)
        Right_Hip_y=sum(Right_Hip_y_List)/len(Right_Hip_y_List)
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x = Right_Hip_x
        results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y = Right_Hip_y  

        # Featured Massage Points
        Mid_Shoulder_x = (Left_Shoulder_x+Right_Shoulder_x)/2
        Mid_Shoulder_y = (Left_Shoulder_y+Right_Shoulder_y)/2

        Mid_Hip_x = (Left_Hip_x+Right_Hip_x)/2
        Mid_Hip_y = (Left_Hip_y+Right_Hip_y)/2

        Center_x = (Mid_Hip_x+Mid_Shoulder_x)/2
        Center_y = (Mid_Hip_y+Mid_Shoulder_y)/2

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        cv2.circle(image,(int(Center_x*image_width),int(Center_y*image_height)),1,(0,255,0),2)
        cv2.circle(image,(int(Mid_Shoulder_x*image_width),int(Mid_Shoulder_y*image_height)),1,(0,255,0),2)
        cv2.circle(image,(int(Mid_Hip_x*image_width),int(Mid_Hip_y*image_height)),1,(0,255,0),2)
        cv2.imwrite('./MassageMate_Vision.png', image)
        # cv2.waitKey() 
        break
  cap.release()
  return (Left_Shoulder_x,Left_Shoulder_y),(Right_Shoulder_x,Right_Shoulder_y),(Left_Hip_x,Left_Hip_y),(Right_Hip_x,Right_Hip_y),(Mid_Hip_x,Mid_Hip_y),(Mid_Shoulder_x,Mid_Shoulder_y),(Center_x,Center_y)


if __name__ == '__main__':

  (Left_Shoulder_x,Left_Shoulder_y),(Right_Shoulder_x,Right_Shoulder_y),(Left_Hip_x,Left_Hip_y),(Right_Hip_x,Right_Hip_y),(Mid_Hip_x,Mid_Hip_y),(Mid_Shoulder_x,Mid_Shoulder_y),(Center_x,Center_y) = human_detection()

  print('Coordinates Detected:')
  print(
      f'Left Shoulder: ('
      f'{Left_Shoulder_x}, '
      f'{Left_Shoulder_y})'
  )

  print(
      f'Right Shoulder: ('
      f'{Right_Shoulder_x}, '
      f'{Right_Shoulder_y})'
  )

  print(
      f'Left Hip: ('
      f'{Left_Hip_x}, '
      f'{Left_Hip_y})'
  )

  print(
      f'Right Hip: ('
      f'{Right_Hip_x}, '
      f'{Right_Hip_y})'
  )

  print(
      f'Mid Hip: ('
      f'{Mid_Hip_x}, '
      f'{Mid_Hip_y})'
  )

  print(
      f'Mid Shoulder: ('
      f'{Mid_Shoulder_x}, '
      f'{Mid_Shoulder_y})'
  )

  print(
      f'Center: ('
      f'{Center_x}, '
      f'{Center_y})'
  )


