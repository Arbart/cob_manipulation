#!/usr/bin/python

import time

import roslib
roslib.load_manifest('cob_gripper_grasp_controller_sdh')
import rospy

from simple_script_server import *
from object_manipulation_msgs.msg import GraspHandPostureExecutionAction
from object_manipulation_msgs.srv import GraspStatus


class cob_gripper_grasp_controller_sdh:

	def __init__(self):
		self.sss = simple_script_server()
		self.action_server = actionlib.SimpleActionServer("/sdh_gripper_grasp_posture_controller", GraspHandPostureExecutionAction, self.execute, False)
		self.query_service = rospy.Service('/sdh_gripper_grasp_status', GraspStatus, self.query_cb)
		self.action_server.start()

	def execute(self, server_goal):
		if server_goal.goal == 2: #GRASP
			if(len(server_goal.grasp.grasp_posture.position) == 0):
				ros.log_err("Empty grasp given")
			else:
				print "moving sdh to grasp ", server_goal.grasp.grasp_posture.position
				self.sss.move("sdh", server_goal.grasp.grasp_posture.position)
				#self.sss.move("sdh", [[0,0,0,0,0,0,0,0]])
		if server_goal.goal == 1: #PRE_GRASP
			if(len(server_goal.grasp.pre_grasp_posture.position) == 0):
				ros.log_err("Empty pregrasp given")
			else:
				print "moving sdh to pregrasp ", server_goal.grasp.pre_grasp_posture.position
				self.sss.move("sdh", server_goal.grasp.pre_grasp_posture.position)
		if server_goal.goal == 3: #RELEASE
			print "received release command"
			self.sss.move("sdh", "cylopen")

	def query_cb(self, req):
		res = GraspStatusResponse()
		res.is_hand_occupied = True
		return res


if __name__ == "__main__":
	rospy.init_node('cob_gripper_grasp_controller_sdh')
	gripper = cob_gripper_grasp_controller_sdh()
	print "Running cob_gripper_grasp_controller_sdh"
	while not rospy.is_shutdown():
		rospy.sleep(1.0)