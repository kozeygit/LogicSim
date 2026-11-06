from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty
from kivy.metrics import dp

KV = '''
#:import chain itertools.chain
FloatLayout:
    Label:
        size_hint_y: None
        text_size: self.width, None
        height: self.texture_size[1]
        pos_hint: {'top': 1}
        color: 0, 0, 0, 1
        padding: 10, 10
        text:
            '\\n'.join((
            'click to create line',
            'click near a point to drag it',
            'click near a line to create a new point in it',
            'double click a point to delete it'
            ))
        canvas.before:
            Color:
                rgba: 1, 1, 1, .8
            Rectangle:
                pos: self.pos
                size: self.size
    BezierCanvas:
<BezierLine>:
    _points: list(chain(*self.points))
    canvas:
        Color:
            rgba: 1, 1, 1, .2
        SmoothLine:
            points: self._points or []
        Color:
            rgba: 1, 1, 1, 1
        Line:
            bezier: self._points or []
            width: 2
        Color:
            rgba: 1, 1, 1, .5
        Point:
            points: self._points or []
            pointsize: 5
'''


def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** .5


class BezierLine(Widget):
    points = ListProperty()
    select_dist = NumericProperty(10)
    delete_dist = NumericProperty(5)

    def on_touch_down(self, touch):
        if super(BezierLine, self).on_touch_down(touch):
            return True

        max_dist = dp(self.select_dist)

        l = len(self.points)

        for i, p in enumerate(self.points):
            if dist(touch.pos, p) < max_dist:
                touch.ud['selected'] = i
                touch.grab(self)
                return True

        for i, p in enumerate(self.points[:-1]):
            if (
                dist(touch.pos, p)
                + dist(touch.pos, self.points[i + 1])
                - dist(p, self.points[i + 1])
                < max_dist
            ):
                self.points = (
                    self.points[:i + 1]
                    + [list(touch.pos)]
                    + self.points[i + 1:]
                )
                touch.ud['selected'] = i + 1
                touch.grab(self)
                return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return super(BezierLine, self).on_touch_move(touch)
        point = touch.ud['selected']

        self.points[point] = touch.pos

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super(BezierLine, self).on_touch_up(touch)
        touch.ungrab(self)
        i = touch.ud['selected']
        if touch.is_double_tap:
            if len(self.points) < 3:
                self.parent.remove_widget(self)
            else:
                self.points = (
                    self.points[:i] + self.points[i + 1:]
                )


class BezierCanvas(Widget):
    def on_touch_down(self, touch):
        if super(BezierCanvas, self).on_touch_down(touch):
            return True

        bezierline = BezierLine()
        bezierline.points = [(touch.pos), (touch.pos)]
        touch.ud['selected'] = 1
        touch.grab(bezierline)
        self.add_widget(bezierline)
        return True


class BezierApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    BezierApp().run()