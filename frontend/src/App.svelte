<script lang="ts">
	import { Router, Link, Route } from "svelte-navigator";
	import {paths} from "./constants"

	import Home from './views/Home.svelte';
	import Login from './views/Login.svelte';
	import Register from './views/Register.svelte';
	
	export let name: string;


</script>

<main>
	<h1>Hello {name}!</h1>
	<Router>
		<nav>
			<Link to={paths.HOME}>Home</Link>
			<Link to={paths.LOGIN}>login</Link>
			<Link to={paths.REGISTER}>Register</Link>
		</nav>
		<div>
			<Route path={paths.HOME}>
				<Home />
			</Route>
			<Route path={paths.LOGIN} component={Login} />
			<Route path={paths.REGISTER} component={Register} />
		</div>
	</Router>
</main>

<style>
</style>
