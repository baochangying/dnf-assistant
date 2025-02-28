from tools.image_deal import screenshot
from tools.image_deal import get_default_region
from tools.image_detect import get_skill_max_lighting
from tools.yolo import YoloPredict
import dnf.keyword_action as act

yolo = YoloPredict("../model/best.pt")


def main():
    skill_max_lighting = get_skill_max_lighting(yolo)
    x, y, w, h = get_default_region()
    # act.buff_skill(skill_max_lighting)
    while True:
        frame = screenshot(x, y, w, h)
        self, monster, material, open_door = yolo.get_cord(frame)
        if len(monster) == 0 and len(material) > 0:
            # 捡材料
            act.pick_material(yolo)
        # 判断是否有开着的门
        if len(open_door) > 0 and len(monster) == 0 and len(material) == 0:
            print("移动到下一个房间")
            act.move_next_room(yolo)
        if len(self) != 0 and len(monster) != 0:
            act.gather_monster_move(yolo, 1)
            frame = screenshot(x, y, w, h)
            self, monster, material, open_door = yolo.get_cord(frame)
            print("开始攻击")
            if len(monster) != 0 and len(self) != 0:
                act.attack(yolo, skill_max_lighting)


if __name__ == '__main__':
    main()
