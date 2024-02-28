import sys
import logging
import cv2 as cv
sys.path.append('../')
from dds_utils import read_results_dict

relevant_classes = ['vehicle']
confidence_threshold = 0.5
max_area_threshold = 0.6

vid_name="D:\\VASRL\\server\\server\\my_dds_sr_619\\dataset\\video_test\\src\\video_test.mp4"
file_name="mv_results"
nomv_file_name="mv_results"
save_name=f"tra.mp4"

def iou(b1, b2):
    # calculate the iou of two bounding boxes
    (x1, y1, w1, h1) = b1
    (x2, y2, w2, h2) = b2
    x3 = max(x1, x2)
    y3 = max(y1, y2)
    x4 = min(x1 + w1, x2 + w2)
    y4 = min(y1 + h1, y2 + h2)
    if x3 > x4 or y3 > y4:
        return 0
    else:
        overlap = (x4 - x3) * (y4 - y3)
        return overlap / (w1 * h1 + w2 * h2 - overlap)

def main():
    # get logger
    logging.basicConfig(
        format="%(name)s -- %(levelname)s -- %(lineno)s -- %(message)s",
        level='INFO')

    logger = logging.getLogger("visualize")
    logger.addHandler(logging.NullHandler())

    results = read_results_dict(file_name)
    nomove_results=read_results_dict(nomv_file_name)
    cap = cv.VideoCapture(vid_name)
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    print(width,height,fps)
    fourcc = cv.VideoWriter_fourcc('H', '2', '6', '4')
    writer = cv.VideoWriter(save_name, fourcc, fps, (width, height))
    fid = -1
    bbox_yx=[]
    while 1:
        ret, frame = cap.read()  # opencvall BGR
        if ret:
            fid = fid + 1
        else:
            print(fid,"end fid")
            break
        if fid % 10 == 0:
            logger.info(f'Visualizing image with frame id {fid}')
            # drawer for this image
        if fid<3:continue
        if fid in results.keys():
            cnt=0
            bbox=results[fid]
            bbox_old=nomove_results[fid]

            for b in bbox_yx:
                cnt+=1
                #需要注释
                b = b.x, b.y, b.w, b.h, b.label, b.conf
                (x, y, w, h, label, confid) = b
                x0 = int(x * width)
                y0 = int(y * height)
                x1 = int((w * width) + x0)
                y1 = int((h * height) + y0)

                # filter out large regions, they are not true objects
                if w * h > max_area_threshold:
                    continue

                # filter out irrelevant regions
                if label not in relevant_classes:
                    continue

                # # filter out low confidence regions
                if confid < confidence_threshold:
                    continue

                cv.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
            for b in bbox_old:
                cnt+=1
                #需要注释
                b = b.x, b.y, b.w, b.h, b.label, b.conf
                (x, y, w, h, label, confid) = b
                x0 = int(x * width)
                y0 = int(y * height)
                x1 = int((w * width) + x0)
                y1 = int((h * height) + y0)

                # filter out large regions, they are not true objects
                if w * h > max_area_threshold:
                    continue

                # filter out irrelevant regions
                if label not in relevant_classes:
                    continue

                # # filter out low confidence regions
                if confid < confidence_threshold:
                    continue

                cv.rectangle(frame, (x0, y0), (x1, y1), (255, 0, 0), 2)
            print(cnt)

        else:
            print(fid,"not detect any object")

        writer.write(frame)

if __name__ == '__main__':
    main()
