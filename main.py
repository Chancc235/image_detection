from process import parse_args, find_images
import json
import cv2
import sys
import logging
import pathlib
from img_detection.detection import detect_blurry
from img_detection.detection import fix_image_size
from img_detection.detection import pretty_blur_map

if __name__ == '__main__':
    assert sys.version_info >= (3, 6), sys.version_info
    args = parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level)

    fix_size = not args.variable_size
    logging.info(f'fix_size: {fix_size}')

    if args.save_path is not None:
        save_path = pathlib.Path(args.save_path)
        assert save_path.suffix == '.json', save_path.suffix
    else:
        save_path = None

    results = []

    for image_path in find_images(args.images):
        image = cv2.imread(str(image_path))
        if image is None:
            logging.warning(f'warning! failed to read image from {image_path}; skipping!')
            continue

        logging.info(f'processing {image_path}')

        if fix_size:
            image = fix_image_size(image)
        else:
            logging.warning('not normalizing image size for consistent scoring!')

        blur_map, score, brightness, blurry, bright = detect_blurry(image, threshold_blur=args.threshold_blur,
                                                             threshold_bright=args.threshold_bright)
        # blur_map, score, brightness, blurry, bright = estimate_blur_and_bright(image,
        #                                                                        threshold_blur=args.threshold_blur,
        #                                                                        threshold_bright=args.threshold_bright)

        logging.info(
            f'image_path: {image_path} score: {score} brightness: {brightness} blurry: {blurry}, bright: {bright}')
        results.append({'input_path': str(image_path), 'score': score, 'brightness': brightness, 'blurry': blurry,
                        'bright': bright})

        if args.display:
            cv2.imshow('input', image)
            cv2.imshow('result', pretty_blur_map(blur_map))

            if cv2.waitKey(0) == ord('q'):
                logging.info('exiting...')
                exit()

    if save_path is not None:
        logging.info(f'saving json to {save_path}')

        with open(save_path, 'w') as result_file:
            data = {'images': args.images, 'threshold_blur': args.threshold_blur,
                    'threshold_bright': args.threshold_bright, 'fix_size': fix_size, 'results': results}
            json.dump(data, result_file, indent=4)
