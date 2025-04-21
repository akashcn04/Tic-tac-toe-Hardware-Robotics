from pyniryo import NiryoRobot, JointsPosition
import time

class RobotController:
    def __init__(self):
        # Initialize with the robot's current IP from NiryoStudio
        self.robot = NiryoRobot("10.10.10.10")  # Updated IP
        self.robot.calibrate_auto()
        self.tool_id = 1  # Kept for potential future use, but not passed to methods
        
        # Define 5cm spacing between grid cells (25 cm²)
        self.cell_size = 0.05  # 5 cm spacing
        
        # Reference center position - moved 8cm further away
        center_x = 0.100
        center_y = -0.180  # 8 cm further away than original
        
        # Lowering the overall z-coordinate by 4cm
        center_z = 0.11  # Original 0.15 minus 0.04 (4cm)
        
        # Calculate grid positions with increased spacing
        self.positions = {
            0: [center_x + self.cell_size, center_y - self.cell_size, center_z],    # Top-left (1)
            1: [center_x,                  center_y - self.cell_size, center_z],    # Top-middle (2)
            2: [center_x - self.cell_size, center_y - self.cell_size, center_z],    # Top-right (3)
            3: [center_x + self.cell_size, center_y,                  center_z],    # Middle-left (4)
            4: [center_x,                  center_y,                  center_z],    # Center (5)
            5: [center_x - self.cell_size, center_y,                  center_z],    # Middle-right (6)
            6: [center_x + self.cell_size, center_y + self.cell_size, center_z],    # Bottom-left (7)
            7: [center_x,                  center_y + self.cell_size, center_z],    # Bottom-middle (8)
            8: [center_x - self.cell_size, center_y + self.cell_size, center_z]     # Bottom-right (9)
        }
        
        # Update yard position z-height also by 4cm lower
        self.yard_position = [0.2, 0.0, 0.11]  # Original 0.15 minus 0.04 (4cm)
        
        # Activate the tool (ensure end effector is recognized)
        self.robot.update_tool()
        
    def calibrate_workspace(self):
        try:
            self.robot.set_arm_max_velocity(100)
            if self.robot.collision_detected:  # Check collision state
                self.robot.clear_collision_detected()
                time.sleep(1)
            self.robot.move_to_home_pose()
            time.sleep(2)
        except Exception as e:
            print(f"Calibration error: {e}")
            self.robot.close_connection()
            raise
            
    def pick_from_yard(self):
        try:
            # Approach yard from above
            self.robot.move_pose(self.yard_position[0], self.yard_position[1], self.yard_position[2] + 0.05, 0, 1.57, 0)
            self.robot.move_pose(*self.yard_position, 0, 1.57, 0)
            time.sleep(1)
            # Open gripper to prepare for picking
            self.robot.release_with_tool()
            time.sleep(1)
            # Close gripper to grasp marker
            self.robot.grasp_with_tool()
            time.sleep(1)
            # Lift marker
            self.robot.move_pose(*self.yard_position, 0, 1.57, 0)
            time.sleep(1)
        except Exception as e:
            print(f"Pick error: {e}")
            if self.robot.collision_detected:
                self.robot.clear_collision_detected()
            raise
            
    def place_at_position(self, move_index):
        try:
            x, y, z = self.positions[move_index]
            # Approach position from above
            self.robot.move_pose(x, y, z + 0.05, 0, 1.57, 0)
            self.robot.move_pose(x, y, z, 0, 1.57, 0)
            time.sleep(1)
            
            # Release marker
            self.robot.release_with_tool()
            time.sleep(1)
            
            # Lift arm for clearance
            self.robot.move_pose(x, y, z + 0.05, 0, 1.57, 0)
            time.sleep(1)
        except Exception as e:
            print(f"Place error: {e}")
            if self.robot.collision_detected:
                self.robot.clear_collision_detected()
            raise
            
    def close(self):
        try:
            self.robot.move_to_home_pose()
            self.robot.close_connection()
        except Exception as e:
            print(f"Close error: {e}")
            
    def __del__(self):
        self.close()