import tkinter as tk
from tkinter import *
from tkinter import filedialog

import win32api
from PIL import Image

from algo import *
from shortcuts import *

tick = pg.image.load(r'tick.png')
tick = pg.transform.scale(tick, (30, 30))

cross = pg.image.load(r'cross.jpg')
cross = pg.transform.scale(cross, (30, 30))

arrow = pg.image.load(r'arrow.png')
arrow = pg.transform.scale(arrow, (30, 30))


def pass_func():
    ...


def to_start():
    global step
    step = 'uploading'


def previous():
    global step
    steps = ['uploading', 'scoping', 'selection', 'classification']
    curr_idx = steps.index(step)
    step = steps[curr_idx - 1]


def next_step():
    global step
    steps = ['uploading', 'scoping', 'selection', 'classification']
    curr_idx = steps.index(step)
    step = steps[curr_idx + 1]


def upload_file():
    global name, step, image_format, scope_rect

    f_types = [('JPG Files', '*.jpg'),
               ('PNG Files', '*.png'),
               ('JPEG Files', '*.jpeg')]  # type of files to select
    filename = tk.filedialog.askopenfilename(filetypes=f_types)
    try:
        img = Image.open(filename)
        pg_img = pg.image.load(filename)
        name = filename.split('/')[-1]
        image_format = name.split('.')[-1]
        img.save(f'images/original.{image_format}')
        step = 'scoping'
        scope_rect = pg.Rect(pg_img.get_rect())
    except AttributeError:
        ...


def to_classification():
    global step
    step = 'classification'
    contour.append(contour[0])
    for i in range(len(contour)):
        contour[i] = (int(contour[i][0] - ((WIDTH - 320 - image.get_width()) // 2 + 10)),
                      int(contour[i][1] - ((HEIGHT - 20 - image.get_height()) // 2 + 10)))
    if len(contour) > 1:
        for i in range(len(contour) - 1):
            cv2.line(cv_image,
                     (int(contour[i][0]), int(contour[i][1])),
                     (int(contour[i + 1][0]), int(contour[i + 1][1])),
                     (0, 0, 255), 10)
    res_img = np.zeros(cv_image.shape[:2])
    res_img = cv2.drawContours(res_img, np.array([contour]), -1, color=(255, 255, 255), thickness=cv2.FILLED)
    cv2.imwrite(f'images/res.{image_format}', cv2.resize(res_img, (scope_rect.width, scope_rect.height)))


def steps_list():
    steps = ['uploading', 'scoping', 'selection', 'classification']
    steps_txt = ['Uploading tumor image', 'Scoping to tumor', "Tumor's contour selection", 'Result']
    step_idx = steps.index(step)
    for i in range(len(steps)):
        if i < step_idx:
            sprite = tick
        elif i == step_idx:
            sprite = arrow
        else:
            sprite = cross
        screen.blit(sprite, (WIDTH - 300, (i + 1) * 50))
        font = pg.font.Font(None, 25)
        txt_surface = font.render(steps_txt[i], True, (0, 0, 0))
        screen.blit(txt_surface, (WIDTH - 300 + sprite.get_width() + 20, (i + 1) * 50 + 10))


# def draw_arrow(position, width, height, color, img):
#     contour_points = list()
#     start_x, start_y = position
#     contour_points.append((start_x, int(start_y+0.25*height)))
#     contour_points.append((int(start_x+0.7*width), int(start_y+0.25*height)))
#     contour_points.append((int(start_x+0.7*width), start_y))
#     contour_points.append((start_x+width, start_y-height//2))
#     contour_points.append((int(start_x + 0.7 * width), start_y + width))
#     contour_points.append(contour_points.append((int(start_x+0.7*width), int(start_y+0.75*height))))
#     contour_points.append((start_x, int(start_y + 0.75 * height)))
#     contour_points.append((start_x, int(start_y + 0.25 * height)))
#     res_img = cv2.drawContours(img, np.array([contour_points]), -1, color=color, thickness=cv2.FILLED)


WIDTH = pg.display.set_mode().get_width()
HEIGHT = pg.display.set_mode().get_height()
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
name = None
image_format = None
step = 'uploading'
contour = list()
classification_finished = False

while True:
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        pass

    steps_list()

    Button(
        position=(WIDTH - 300, HEIGHT - 70),
        text='QUIT',
        action=exit,
        font_size=25,
        width=280,
        height=50,
        color=(255, 0, 0)
    ).draw(surface=screen)

    if step == 'uploading':
        Button(
            position=((WIDTH - 320 - 200) // 2, (HEIGHT - 20 - 50) // 2),
            text='Upload Image',
            action=upload_file,
            font_size=30,
            width=200,
            height=50
        ).draw(surface=screen)

        Button(
            position=(WIDTH - 300, HEIGHT - 190),
            text='PREVIOUS',
            action=pass_func,
            font_size=25,
            width=280,
            height=50,
            color=(255, 165, 0),
            active=False
        ).draw(surface=screen)

        Button(
            position=(WIDTH - 300, HEIGHT - 130),
            text='NEXT',
            action=next_step,
            font_size=25,
            width=280,
            height=50,
            color=(0, 255, 0),
            active=False
        ).draw(surface=screen)
        start_scoping = False

    elif step == 'scoping':

        Button(
            position=(WIDTH - 300, HEIGHT - 190),
            text='PREVIOUS',
            action=previous,
            font_size=25,
            width=280,
            height=50,
            color=(255, 165, 0)
        ).draw(surface=screen)
        if not start_scoping:
            Button(
                position=(WIDTH - 300, HEIGHT - 130),
                text='NEXT',
                action=next_step,
                font_size=25,
                width=280,
                height=50,
                color=(0, 255, 0)
            ).draw(surface=screen)
        else:
            Button(
                position=(WIDTH - 300, HEIGHT - 130),
                text='NEXT',
                action=next_step,
                font_size=25,
                width=280,
                height=50,
                color=(0, 255, 0),
                active=False
            ).draw(surface=screen)

        image = pg.image.load(f'images/original.{image_format}')
        cv_image = cv2.imread(f'images/original.{image_format}')
        cv2.imwrite(f'images/scoped.{image_format}', cv_image)
        pil_image = Image.open(f'images/original.{image_format}')
        img_width = image.get_width()
        img_height = image.get_height()
        first_scale = min((WIDTH - 320) / img_width, (HEIGHT - 20) / img_height)
        image = pg.transform.scale(image, (img_width * first_scale, img_height * first_scale))
        pil_image = pil_image.resize((int(img_width * first_scale), int(img_height * first_scale)))
        cv_image = cv2.resize(cv_image, (int(img_width * first_scale), int(img_height * first_scale)))
        screen.blit(image,
                    (((WIDTH - 320 - image.get_width()) // 2 + 10), ((HEIGHT - 20 - image.get_height()) // 2 + 10)))

        if dot_in_rectangle(rect=screen_rect, dot=pg.mouse.get_pos()):
            for event in pg.event.get():
                if pg.key.get_pressed()[pg.K_ESCAPE]:
                    start_scoping = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    left = win32api.GetKeyState(0x001)
                    if left in [-127, -128]:
                        if not start_scoping:
                            scope_x, scope_y = pg.mouse.get_pos()
                            start_scoping = True
                        else:

                            start_x = scope_rect.x - ((WIDTH - 320 - image.get_width()) // 2 + 10)
                            start_y = scope_rect.y - ((HEIGHT - 20 - image.get_height()) // 2 + 10)
                            scope_image = pil_image.crop(
                                (
                                    start_x,
                                    start_y,
                                    start_x + scope_rect.width,
                                    start_y + scope_rect.height
                                )
                            )
                            scope_image.save(f'images/scoped.{image_format}')
                            scope_image = cv2.imread(f'images/scoped.{image_format}')
                            start_scoping = False
                            step = 'selection'

        if start_scoping:
            scope_w = pg.mouse.get_pos()[0] - scope_x
            scope_h = pg.mouse.get_pos()[1] - scope_y
            if scope_x + scope_w >= screen_rect.x + screen_rect.width:
                scope_w = screen_rect.x + screen_rect.width - scope_x
            if scope_y + scope_h >= screen_rect.y + screen_rect.height:
                scope_h = screen_rect.y + screen_rect.height - scope_y
            scope_rect = pg.Rect(scope_x, scope_y, scope_w, scope_h)
            if scope_w < 0:
                scope_rect.x += scope_w
                scope_rect.width *= -1
            if scope_h < 0:
                scope_rect.y += scope_h
                scope_rect.height *= -1
            pg.draw.rect(surface=screen, rect=scope_rect, color=(255, 0, 0), width=3)

            text = 'ESC - cancel scoping'
            font = pg.font.Font(None, 30)
            txt_surface = font.render(text, True, (255, 0, 0))
            screen.blit(txt_surface, (20, HEIGHT - 35))

        contour = list()

    elif step == 'selection':
        Button(
            position=(WIDTH - 300, HEIGHT - 190),
            text='PREVIOUS',
            action=previous,
            font_size=25,
            width=280,
            height=50,
            color=(255, 165, 0)
        ).draw(surface=screen)

        image = pg.image.load(f'images/scoped.{image_format}')
        cv_image = cv2.imread(f'images/scoped.{image_format}')
        pil_image = Image.open(f'images/scoped.{image_format}')
        img_width = image.get_width()
        img_height = image.get_height()
        second_scale = min((WIDTH - 320) / img_width, (HEIGHT - 20) / img_height)
        image = pg.transform.scale(image, (img_width * second_scale, img_height * second_scale))
        pil_image = pil_image.resize((int(img_width * second_scale), int(img_height * second_scale)))
        cv_image = cv2.resize(cv_image, (int(img_width * second_scale), int(img_height * second_scale)))
        screen.blit(image,
                    (((WIDTH - 320 - image.get_width()) // 2 + 10), ((HEIGHT - 20 - image.get_height()) // 2 + 10)))

        if dot_in_rectangle(rect=screen_rect, dot=pg.mouse.get_pos()):
            for event in pg.event.get():
                if len(contour):
                    if pg.key.get_pressed()[pg.K_z] and pg.key.get_pressed()[pg.K_LCTRL]:
                        del contour[-1]
                        time.sleep(0.2)
                if event.type == pg.MOUSEBUTTONDOWN:
                    left = win32api.GetKeyState(0x001)
                    if left in [-127, -128]:
                        contour.append(pg.mouse.get_pos())
                        # if len(contour) > 1:
                        #     cv2.line(cv_image, contour[-1], contour[-2], (255, 0, 0), 3)

        for i in range(len(contour)):
            pg.draw.circle(screen, (255, 0, 0), contour[i], 3)
            if i + 1 != len(contour):
                pg.draw.line(screen, (255, 0, 0), contour[i], contour[i + 1], 3)
            else:
                pg.draw.line(screen, (255, 0, 0), contour[-1], contour[0], 3)

        if len(contour):
            text = 'CTRL+Z - delete last point'
            font = pg.font.Font(None, 30)
            txt_surface = font.render(text, True, (255, 0, 0))
            screen.blit(txt_surface, (20, HEIGHT - 35))

        if len(contour) >= 3:
            Button(
                position=(WIDTH - 300, HEIGHT - 130),
                text='NEXT',
                action=to_classification,
                font_size=25,
                width=280,
                height=50,
                color=(0, 255, 0)
            ).draw(surface=screen)
        else:
            Button(
                position=(WIDTH - 300, HEIGHT - 130),
                text='NEXT',
                action=to_classification,
                font_size=25,
                width=280,
                height=50,
                color=(0, 255, 0),
                active=False
            ).draw(surface=screen)
        classification_finished = False

    elif step == 'classification':
        if not classification_finished:
            img = cv2.imread(f'images/res.{image_format}')
            predicted_class = predict(img)
            classification_finished = True
        Button(
            position=(WIDTH - 300, HEIGHT - 130),
            text='AGAIN',
            action=to_start,
            font_size=25,
            width=280,
            height=50,
            color=(0, 255, 0)
        ).draw(surface=screen)

        result_image = pg.image.load(f'images/res.{image_format}')
        scoped_image = pg.image.load(f'images/scoped.{image_format}')
        first_rect = pg.Rect(int(screen_rect.x + screen_rect.width * 0.1),
                             int(screen_rect.y + screen_rect.height * 0.2),
                             int(screen_rect.width * 0.3),
                             int(screen_rect.height * 0.3))
        second_rect = pg.Rect(int(screen_rect.x + screen_rect.width * 0.6),
                              int(screen_rect.y + screen_rect.height * 0.2),
                              int(screen_rect.width * 0.3),
                              int(screen_rect.height * 0.3))

        scale = min(first_rect.width / result_image.get_width(), first_rect.height / result_image.get_height())
        result_image = pg.transform.scale(result_image,
                                          (result_image.get_width() * scale, result_image.get_height() * scale))
        scoped_image = pg.transform.scale(scoped_image,
                                          (scoped_image.get_width() * scale, scoped_image.get_height() * scale))

        screen.blit(scoped_image, (int((first_rect.width - scoped_image.get_width()) // 2 + first_rect.x),
                    int((first_rect.height - scoped_image.get_height()) // 2 + first_rect.y)))

        screen.blit(result_image, (int((second_rect.width - result_image.get_width()) // 2 + second_rect.x),
                    int((first_rect.height - result_image.get_height()) // 2 + second_rect.y)))

        pg.draw.rect(screen, (0, 0, 0), first_rect, 3)
        pg.draw.rect(screen, (0, 0, 0), second_rect, 3)

        # screen.blit(scoped_image, ())
        if predicted_class == 0:
            text = 'BENIGN'
            color = (0, 255, 0)
        elif predicted_class == 1:
            text = 'MALIGNANT'
            color = (255, 0, 0)
        else:
            text = 'ADDITIONAL EXAMINATION'
            color = (255, 165, 0)
        font = pg.font.Font(None, 100)
        txt_surface = font.render(text, True, color)
        screen.blit(txt_surface, (
            ((WIDTH - txt_surface.get_width() - 320) // 2), ((HEIGHT - txt_surface.get_height()) // 2 + HEIGHT * 0.15)))

    screen_rect = pg.Rect(10, 10, WIDTH - 320, HEIGHT - 20)
    pg.draw.rect(
        rect=screen_rect,
        color=(0, 0, 0),
        width=2,
        surface=screen
    )
    pg.display.update()
