<script lang="ts">
  import { Router, Link, Route } from "svelte-navigator";
  import { paths } from "./constants";
  import { user } from "./stores";
  import Home from "./views/Home.svelte";
  import SignIn from "./views/SignIn.svelte";
  import Onboarding from "./views/Onboarding.svelte";
  import Register from "./views/Register.svelte";
  import OauthCallback from "./views/OauthCallback.svelte";
</script>

<style>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--gap-md) var(--gap-lg);
  }

  main {
    padding: var(--gap-lg);
  }

  nav {
    text-transform: uppercase;
  }
</style>

<Router>
  <header>
    <h1>whispers</h1>
    <nav>
      {#if $user}
        <Link to={paths.HOME}>Home</Link>
      {:else}
        <Link to={paths.SIGN_IN}>Sign in</Link>
        <Link to={paths.REGISTER}>Register</Link>
      {/if}
    </nav>
  </header>
  <main>
    {#if $user}
      <Route path={paths.HOME}>
        <Home />
      </Route>
      <Route path={paths.OAUTH_GOOGLE_CALLBACK}>
        <OauthCallback name="Youtube" />
      </Route>
    {:else}
      <Route path={paths.SIGN_IN} component={SignIn} />
      <Route path={paths.REGISTER} component={Register} />
      <Route path={paths.ONBOARDING} component={Onboarding} />
    {/if}
  </main>
</Router>
