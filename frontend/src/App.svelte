<script lang="ts">
  import { Router, Link, Route } from "svelte-navigator";
  import { paths } from "./constants";
  import { user } from "./stores";
  import Home from "./views/Home.svelte";
  import SignIn from "./views/SignIn.svelte";
  import Onboarding from "./views/Onboarding.svelte";
  import Register from "./views/Register.svelte";

  export let name: string;
</script>

<style>
</style>

<main>
  <h1>Hello {name}!</h1>
  <Router>
    <nav>
      {#if $user}
        <Link to={paths.HOME}>Home</Link>
      {:else}
        <Link to={paths.SIGN_IN}>Sign in</Link>
        <Link to={paths.REGISTER}>Register</Link>
      {/if}
    </nav>
    <div>
      {#if $user}
        <Route path={paths.HOME}>
          <Home />
        </Route>
      {:else}
        <Route path={paths.SIGN_IN} component={SignIn} />
        <Route path={paths.REGISTER} component={Register} />
        <Route path={paths.ONBOARDING} component={Onboarding} />
      {/if}
    </div>
  </Router>
</main>
