#!/usr/bin/env python

from Tkinter import *
from Tkinter import PhotoImage
import tkMessageBox
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion
from tf.transformations import quaternion_from_euler
import time

def create_goal(x, y, w):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    q = quaternion_from_euler(0, 0, w)
    goal.target_pose.pose.orientation = Quaternion(*q)

    return goal

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.start = Button(self, height=15, width=35)
        self.start["text"] = "START"
        self.start["command"] = self.select_destination
        self.start.grid(row=0, column=0)

        self.quit = Button(self, text="QUIT", fg="red",
                              command=self.master.destroy, height=15, width=35)
        self.quit.grid(row=0, column=1)

    def select_destination(self):
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="Select the destination:").grid(row=0)

        self.goal_poses = {
            "A": (4.769, -0.299, -0.007),
            "B": (2.140, 3.401, 0.019),
            "C": (-3.889, 3.668, -3.123),
        }

        i = 1
        for name in self.goal_poses.keys():
            button = Button(self, text=name, command=lambda name=name: self.send_goal(name), height=10, width=15)
            button.grid(row=i)
            i += 1

    def send_goal(self, destination):
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="Waiting for server...").grid(row=0)
        self.update()

        client.wait_for_server()

        Label(self, text="Delivery in progress...").grid(row=0)

        x, y, w = self.goal_poses[destination]
        goal = create_goal(x, y, w)

        client.send_goal(goal)
        client.wait_for_result()

        self.return_to_start()

    def return_to_start(self):
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="Returning...").grid(row=0)

        goal = create_goal(0.000, -0.023, 0.017)
        client.send_goal(goal)
        client.wait_for_result()

        Label(self, text="Delivery complete!").grid(row=1)
        time.sleep(5)

        self.create_widgets()


if __name__ == "__main__":
    rospy.init_node('delivery_gui')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    root = Tk()
    app = Application(master=root)
    app.mainloop()

