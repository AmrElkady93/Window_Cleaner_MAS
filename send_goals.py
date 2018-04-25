#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client(x, y,w,z):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y	
    goal.target_pose.pose.orientation.w = w
    goal.target_pose.pose.orientation.z = z

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


if __name__ == '__main__':
    try:
        # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        x = 0.9
        y = 0.9

	obstacles_x = [2.00, 2.00, 6.00, 6.00]	
	obstacles_y = [3.00, 6.26, 3.00, 6.26]

        for i in range(12):
            for j in range(25):
		isObstacle = False
		for k in range(4):
			if x - obstacles_x[k] > 0 and x - obstacles_x[k] < 1.8 and y - obstacles_y[k] > 0 and y - obstacles_y[k] < 1.8 :
				isObstacle = True
				break
                if x > 0.7 and x < 9.34 and y > 0.7 and y < 9.34 and (not isObstacle):
                    result = movebase_client(x, y,1.0,0.0)
                    print (x,y)
                    if result:
                        rospy.loginfo("Goal execution done!")
                x = x+0.4
            y = y+0.4
            for j in range(25):
		isObstacle = False
		for k in range(4):
			if x - obstacles_x[k] > 0 and x - obstacles_x[k] < 1.8 and y - obstacles_y[k] > 0 and y - obstacles_y[k] < 1.8 :
				isObstacle = True
				break
                if x > 0.7 and x < 9.34 and y > 0.7 and y < 9.34 and (not isObstacle):
                    result = movebase_client(x, y,0.0,1.0)
                    print (x,y)
                    if result:
                        rospy.loginfo("Goal execution done!")
                x = x - 0.4
            y = y + 0.4

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
