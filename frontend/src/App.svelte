<script lang="ts">
	import { Router, Link, Route } from "svelte-navigator";
	import Home from './views/Home.svelte';
	import Login from './views/Login.svelte';
	import Register from './views/Register.svelte';
	
	export let name: string;


</script>

<main>
	<h1>Hello {name}!</h1>
	<Router>
		<nav>
			<Link to="/">Home</Link>
			<Link to="login">login</Link>
			<Link to="register">Register</Link>
		</nav>
		<div>
			<Route path="/">
				<Home />
			</Route>
			<Route path="login" component={Login} />
			<Route path="register" component={Register} />
		</div>
	</Router>
</main>

<style>
</style>
