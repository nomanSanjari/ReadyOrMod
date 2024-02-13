import React from "react";
import styled from "styled-components";

const NavbarContainer = styled.div`
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 10px;
	background-color: #333;
	color: white;
`;

const AppName = styled.h1`
	margin: 0;
`;

const UserIcon = styled.img`
	width: 40px;
	height: 40px;
	border-radius: 50%;
`;

const Navbar = ({ appName, userAvatar }) => {
	return (
		<NavbarContainer>
			<AppName>{appName}</AppName>
			{userAvatar && <UserIcon src={userAvatar} alt="User Avatar" />}
		</NavbarContainer>
	);
};

export default Navbar;
