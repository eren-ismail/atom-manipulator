# Author: Ismail Eren
# 
# Description: This is a simple script that adds alters the coordinates of your selected atom for an XYZ file.
# You can either translate an atom or rotate it.

# Usage
# Please enter "1" for translate or "2" for rotate.
# Then enter the name of your xyz file.

# If you select translation, then enter the distances for each coordinate. For example "-2.4 0 4 for" x y z.
# Then enter the atom number which is you can see from list of order from xyz file or a visualization software (e.g. Vesta)
# New file will be saved as with an extansion of _new.xyz

# If you select rotation, then enter the angle in degrees you want to rotate. For example "90"
# Enter the axis which you want around the rotate. Only enter one axis. For example "z" or "X".
# Enter the atom you want to rotate.
# Enter the reference atom which you around to rotate.
 
import re
import numpy as np

# Ask user for the choice
user_choice=int(input("Would you like to translate(1) or rotate(2) an atom: "))
# Ask the XYZ filename
filename = input("Please Enter the XYZ Filename (without extension): ")

# Defining translation function
def translate_atom(filename):
    distances = input("Please Enter the distances you want to modify (x y z): ")
    distances = distances.strip().split()
    dx = float(distances[0])
    dy = float(distances[1])
    dz = float(distances[2])    
    atom_number = int(input("Please Enter the Atom Number: "))
    atom_no = atom_number + 1
  
    with open(f"{filename}.xyz", "r") as file:
        lines = file.readlines()

    with open(f"{filename}_new.xyz", "w") as new_file:
        new_file.writelines(lines[0:atom_no])

        pattern = re.compile(r'\s+')
        coordinates = pattern.split(lines[atom_no].strip())

        selected_atom_x = float(coordinates[1]) + dx
        selected_atom_y = float(coordinates[2]) + dy
        selected_atom_z = float(coordinates[3]) + dz

        lines[atom_no] = f"{coordinates[0]}\t{selected_atom_x:.10f}\t{selected_atom_y:.10f}\t{selected_atom_z:.10f}\n"
        new_file.writelines(lines[atom_no:])


# Defining rotation function
def rotate_atom(filename):
    def rotate_point_3d(x, y, z, angle_degrees, axis, ref_coordinates):
        # Convert angle from degrees to radians
        angle_radians = np.radians(angle_degrees)

        # Translate coordinates to be relative to the reference point
        x -= ref_coordinates[0]
        y -= ref_coordinates[1]
        z -= ref_coordinates[2]

        # Define the 3D rotation matrix based on the specified axis
        if axis.lower() == 'x':
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(angle_radians), -np.sin(angle_radians)],
                [0, np.sin(angle_radians), np.cos(angle_radians)]
            ])
        elif axis.lower() == 'y':
            rotation_matrix = np.array([
                [np.cos(angle_radians), 0, np.sin(angle_radians)],
                [0, 1, 0],
                [-np.sin(angle_radians), 0, np.cos(angle_radians)]
            ])
        elif axis.lower() == 'z':
            rotation_matrix = np.array([
                [np.cos(angle_radians), -np.sin(angle_radians), 0],
                [np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1]
            ])
        else:
            raise ValueError("Invalid axis. Use 'x', 'y', or 'z'.")

        # Create a column vector for the original coordinates
        original_point = np.array([x, y, z])

        # Perform the 3D rotation
        rotated_point = np.dot(rotation_matrix, original_point)

        # Translate back to the original coordinates
        rotated_point[0] += ref_coordinates[0]
        rotated_point[1] += ref_coordinates[1]
        rotated_point[2] += ref_coordinates[2]

        return rotated_point

    rotation_angle = float(input("Please Enter the angle(in degrees): "))
    rotation_axis  = input("Please Enter the axis which you want it around to rotate (x y z) : ")
    
    atom_number = int(input("Please Enter the Atom Number of you want to rotate: "))
    atom_no = atom_number + 1
    
    ref_atom_number = int(input("Please Enter the Reference Atom Number of you want around rotate: "))
    ref_atom_no = ref_atom_number + 1
  
    with open(f"{filename}.xyz", "r") as file:
        lines = file.readlines()

    with open(f"{filename}_new.xyz", "w") as new_file:
        new_file.writelines(lines[0:atom_no])

        pattern = re.compile(r'\s+')
        coordinates = pattern.split(lines[atom_no].strip())
        ref_coordinates = pattern.split(lines[ref_atom_no].strip())

        # Extract x, y, z coordinates
        x, y, z = map(float, coordinates[1:4])

        # Perform the rotation
        rotated_point = rotate_point_3d(x, y, z, rotation_angle, rotation_axis, list(map(float, ref_coordinates[1:4])))

        # Update the coordinates in the line
        lines[atom_no] = f"{coordinates[0]}\t{rotated_point[0]:.10f}\t{rotated_point[1]:.10f}\t{rotated_point[2]:.10f}\n"
        
        new_file.writelines(lines[atom_no:])



# usage
if user_choice == 1:
    translate_atom(filename)
elif user_choice == 2:
    rotate_atom(filename)


