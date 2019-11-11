import cv2
import algorithms
import numpy as np
from blob import Blob
from beer import Beer

cap = cv2.VideoCapture("recordings/test2_gameplay2.mp4")

beer_template_left = cv2.imread("images/beer_reg_left.jpg")
beer_template_right = cv2.imread("images/beer_reg_right.jpg")


if __name__ == "__main__":
    # UI.UI().run()
    # crop -> get size -> get beer positions

    beers_centers_10_left = [[20, 21], [70, 18], [118, 15], [170, 12], [43, 64], [93, 61], [142, 56], [67, 107],
                              [118, 102], [92, 147]]

    beers_centers_10_right = [[11, 144], [60, 148], [109, 150], [158, 150], [33, 101], [84, 107], [133, 107], [64, 61],
                              [113, 62], [91, 21]]

    beers_left = []
    for i in range(0, 10):
        beers_left.append(Beer(beers_centers_10_left[i]))

    beers_right = []
    for i in range(0, 10):
        beers_right.append(Beer(beers_centers_10_right[i]))

    while cap.isOpened():

        _, frame = cap.read()

        # ---------- MIDDLE AREA

        middle_area = frame[130:350, 220:420]


        # cv2.imshow("middle area", middle_area)

        # ----------- BEER AREA LEFT

        beer_area_left = frame[130:350, 0:220]

        beers_regular_left = algorithms.matchTemplate(beer_area_left, beer_template_left)
        # beers_highlighted = algorithms.matchTemplate(beer_area, beer_template)
        # beers_foam = algorithms.matchTemplate(beer_area, beer_template)
        # ... different templates / different color thresholds to find all the beers

        # beers_likelihood = beers_classic || beers_highlighted || beers_foam
        # ... all the found beers combined
        beers_likelihood_left = beers_regular_left  # for now we just look for the classic non-highlighted beer

        beers_binary_left = algorithms.threshold(beers_likelihood_left, 0.4, 1)
        blobs_left = algorithms.extractBlobs(np.copy(beers_binary_left))

        algorithms.informBeers(beers_left, blobs_left, beer_area_left)

        # ------------- BEER AREA RIGHT

        beer_area_right = frame[130:350, 420:640]
        beers_regular_right = algorithms.matchTemplate(beer_area_right, beer_template_right)
        # beers_highlighted = algorithms.matchTemplate(beer_area, beer_template)
        # beers_foam = algorithms.matchTemplate(beer_area, beer_template)
        # ... different templates / different color thresholds to find all the beers

        # beers_likelihood = beers_classic || beers_highlighted || beers_foam
        # ... all the found beers combined
        beers_likelihood_right = beers_regular_right  # for now we just look for the classic non-highlighted beer

        beers_binary_right = algorithms.threshold(beers_likelihood_right, 0.4, 1)
        blobs_right = algorithms.extractBlobs(np.copy(beers_binary_right))

        algorithms.informBeers(beers_right, blobs_right, beer_area_right)




        # -------------- RESULT

        result = np.zeros([50, 150, 3], np.uint8)
        result_beer_centers_left = [[10, 10], [10, 20], [10, 30], [10, 40], [20, 15], [20, 25], [20, 35], [30, 20],
                                   [30, 30], [40, 25]]

        result_beer_centers_right = [[140, 10], [140, 20], [140, 30], [140, 40], [130, 15], [130, 25], [130, 35], [120, 20],
                                    [120, 30], [110, 25]]

        for i in range(0, len(result_beer_centers_left)):
            if beers_left[i].is_present:
                if beers_left[i].green_ball:
                    cv2.circle(result, (result_beer_centers_left[i][0], result_beer_centers_left[i][1]), 3, (0, 255, 0), -1)
                elif beers_left[i].red_ball:
                    cv2.circle(result, (result_beer_centers_left[i][0], result_beer_centers_left[i][1]), 3, (0, 0, 255), -1)
                else:
                    cv2.circle(result, (result_beer_centers_left[i][0], result_beer_centers_left[i][1]), 3, (255, 255, 255), -1)

        for i in range(0, len(result_beer_centers_right)):
            if beers_right[i].is_present:
                if beers_right[i].green_ball:
                    cv2.circle(result, (result_beer_centers_right[i][0], result_beer_centers_right[i][1]), 3, (0, 255, 0), -1)
                elif beers_right[i].red_ball:
                    cv2.circle(result, (result_beer_centers_right[i][0], result_beer_centers_right[i][1]), 3, (0, 0, 255), -1)
                else:
                    cv2.circle(result, (result_beer_centers_right[i][0], result_beer_centers_right[i][1]), 3, (255, 255, 255), -1)

        # for beer in beers_right:
        #     end_point_y = beer.ideal_center[0] + 40 if beer.ideal_center[0] + 40 < beer_area_right.shape[0] else \
        #     beer_area_right.shape[0]
        #     end_point_x = beer.ideal_center[1] + 40 if beer.ideal_center[1] + 40 < beer_area_right.shape[1] else \
        #     beer_area_right.shape[1]
        #
        #     beer_area_right[beer.ideal_center[0]:end_point_y, beer.ideal_center[1]:end_point_x] = (255, 0, 0)
        #
        # for beer in beers_left:
        #     end_point_y = beer.ideal_center[0] + 40 if beer.ideal_center[0] + 40 < beer_area_left.shape[0] else \
        #     beer_area_left.shape[0]
        #     end_point_x = beer.ideal_center[1] + 40 if beer.ideal_center[1] + 40 < beer_area_left.shape[1] else \
        #     beer_area_left.shape[1]
        #
        #     beer_area_left[beer.ideal_center[0]:end_point_y, beer.ideal_center[1]:end_point_x] = (255, 0, 0)

        # cv2.imshow("beers binary left", beers_binary_left)
        # cv2.imshow("beers binary right", beers_binary_right)
        cv2.imshow("beer area left", beer_area_left)
        cv2.imshow("beer area right", beer_area_right)
        cv2.imshow("result", result)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# TODO keep track of the history of detection (was this beer detected at least once in the last 20 frames?)
# TODO detect rounds
# TODO dynamic UI (map computer vision findings to the UI)
# TODO database of players
