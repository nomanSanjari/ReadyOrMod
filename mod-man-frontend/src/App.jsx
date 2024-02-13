import React from "react";
import { Container } from "./components/styled/Container.styled";
import { Navbar } from "./components/styled/Navbar.styled";

function App() {
	const appName = "Mod-Man";
	const userAvatar = "../public/user-avatar.svg";

	return (
		<>
			<Container>
				<Navbar appName={appName} userAvatar={userAvatar} />
				<h1>Hello, World!</h1>
			</Container>
		</>
	);
}

export default App;
