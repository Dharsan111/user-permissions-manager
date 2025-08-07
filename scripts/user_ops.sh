#!/bin/bash 

case "$1" in
	add_user)
		sudo useradd "$2" && echo "User '$2' added." || echo "Error adding User."
		;;
	remove_user)
		sudo userdel "$2" && echo "User '$2' removed." || echo "Error removing User."
		;;
	add_group)
		sudo groupadd "$2" && echo "Group '$2' added." || echo "Error adding Group."
		;;
	remove_group)
		sudo groupdel "$2" && echo "Group '$2' removed." || echo "Error removing Group."
		;;
	list_users)
		cut -d: -f1 /etc/passwd
		;;
	list_groups)
		cut -d: -f1 /etc/group
		;;
	change_password)
		echo "$2:$3" | sudo chpasswd && echo "Password changed for $2." || echo "Error changing Password"
		;;
	add_user_to_group)
		sudo usermod -aG "$3" "$2" && echo "Added $2 to $3." || echo "Error adding user to group."
		;;
	chmod)
		sudo chmod "$2" "$3" && echo "Permissions set." || echo "Error setting Permissions."
		;;
	*)
		echo "Invalid Command."
		exit 1
		;;
esac
