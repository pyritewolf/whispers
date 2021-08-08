<script lang="ts">
	import { Router, Link, Route } from "svelte-navigator";
	import Home from './views/Home.svelte';
	import Login from './views/Login.svelte';
	
	export let name: string;

</script>

<main>
	<h1>Hello {name}!</h1>
	<Router>
		<nav>
			<Link to="/">Home</Link>
			<Link to="login">login</Link>
		</nav>
		<div>
			<Route path="/">
				<Home />
			</Route>
			<Route path="login" component={Login} />
		</div>
	</Router>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
