<script lang="ts">
  import { onMount } from "svelte";
  import { Route, navigate } from "svelte-navigator";
  import { user } from "../stores";
  import { paths } from "../constants";

  export let condition: boolean = !!$user;
  export let redirectTo: string = paths.SIGN_IN;
  export let path: string;
  export let component = null;

  onMount(() => {
    if (!condition) navigate(redirectTo);
  });
</script>

{#if condition}
  <Route {path} {component}>
    <slot />
  </Route>
{/if}
