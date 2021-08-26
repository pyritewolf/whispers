<script lang="ts">
  import { Router, Link, Route } from "svelte-navigator";
  import { paths } from "./constants";
  import { api, user } from "./stores";
  import {
    Home,
    OauthCallback,
    SignIn,
    PasswordRecovery,
    Onboarding,
    Register,
    SetNewPassword,
    Chat,
  } from "./views";

  const signOut = async () => {
    await $api("/auth/signout");
    user.set(null);
    window.location.replace(paths.SIGN_IN);
  };
</script>

<style>
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--gap-md) var(--gap-lg);
  }

  header :global(.logo) {
    color: var(--white);
    text-decoration: none !important;
    transition: var(--transition);
  }

  header h1::first-letter {
    text-shadow: -0.8rem 0 0 var(--dark-primary);
    transition: var(--transition);
  }

  header h1:hover::first-letter {
    text-shadow: -0.8rem 0 0 var(--dark-secondary);
    transition: var(--transition);
  }

  main {
    padding: var(--gap-lg);
  }

  nav {
    text-transform: uppercase;
  }

  nav span {
    color: var(--primary);
    font-weight: bold;
    cursor: pointer;
  }

  nav span:hover {
    text-decoration: underline;
  }
</style>

<Router>
  <header>
    <Link class="logo" to={paths.HOME}>
      <h1>whispers</h1>
    </Link>
    <nav>
      {#if $user}
        <Link to={paths.HOME}>Home</Link>
        <span on:click={signOut}>Sign out</span>
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
      <Route path={`${paths.CHAT}`}>
        <Chat streamer={$user.username} />
      </Route>
    {:else}
      <Route path={paths.REGISTER} component={Register} />
    {/if}
    <Route path={paths.PASSWORD_RECOVERY} component={PasswordRecovery} />
    <Route path={paths.NEW_PASSWORD} component={SetNewPassword} />
    <Route path={paths.SIGN_IN} component={SignIn} />
    <Route path={paths.ONBOARDING} component={Onboarding} />
    <!-- <Route path={`${paths.CHAT}/:streamer`} component={Chat} /> -->
  </main>
</Router>
