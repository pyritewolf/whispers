<script lang="ts">
  import { Link, navigate } from "svelte-navigator";
  import { paths } from "../constants";
  import { api, user } from "../stores";

  const signOut = async () => {
    await $api("/auth/signout");
    user.set(null);
    navigate(paths.SIGN_IN);
  };
</script>

<style>
  .root {
    background-color: var(--darkest-gray);
    min-height: 100vh;
  }

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
    text-shadow: -0.8rem 0 0 var(--primary);
    transition: var(--transition);
  }

  header h1:hover::first-letter {
    text-shadow: -0.8rem 0 0 var(--secondary);
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

<div class="root">
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
    <slot />
  </main>
</div>
