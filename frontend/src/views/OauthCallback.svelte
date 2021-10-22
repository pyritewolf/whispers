<script lang="ts">
  import { Link, navigate } from "svelte-navigator";
  import { api, user } from "../stores";
  import AuthLayout from "../layouts/AuthLayout.svelte";
  import Icon from "../components/Icon.svelte";
  import { APIStatus, Gap, getErrorFor, NormalIcon } from "../types/components";
  import { paths } from "../constants";

  export let name: string;
  let seconds: number = 5;

  const token = new URLSearchParams(window.location.search).get("code");

  const startCountdown = (sec: number = 5): void => {
    seconds = sec;
    if (sec > 1)
      setTimeout(() => {
        startCountdown(sec - 1);
      }, 1000);
    else
      setTimeout(() => {
        navigate(paths.HOME);
      }, 1000);
  };

  const verifyToken = async () => {
    if (!token) throw Error("Uh-oh. Auth failed.");
    const result = await $api("/auth/google/callback", {
      method: "POST",
      body: JSON.stringify({ token }),
    });
    if (result.status === APIStatus.ok) {
      startCountdown();
      user.set(result.body);
    }
    return result;
  };

  const promise = verifyToken();
</script>

<style>
  h1 {
    text-align: center;
    padding-bottom: var(--gap-md);
  }

  p {
    text-align: center;
    padding-bottom: var(--gap-md);
  }
</style>

<AuthLayout>
  {#await promise}
    <p>
      <Icon name={NormalIcon.newspaper} size={Gap.xl} />
    </p>
    <h1>One sec!</h1>
    <p>Finishing your connection with {name}...</p>
  {:then response}
    {#if response.status === APIStatus.ok}
      <p>
        <Icon name={NormalIcon.thumbs_up} size={Gap.xl} />
      </p>
      <h1>All good!</h1>
      <p>Yey! Your {name} account is linked.</p>
      <p>
        We'll take you to the home in
        {seconds}
        seconds, or you can
        <Link to={paths.HOME}>click here</Link>.
      </p>
    {:else}
      <p>
        <Icon name={NormalIcon.skull_crossbones} size={Gap.xl} />
      </p>
      <h1>Damn</h1>
      <p>{getErrorFor('oauth', response.body)}</p>
      <p>Try again later, please!</p>
    {/if}
  {:catch error}
    <p>
      <Icon name={NormalIcon.skull_crossbones} size={Gap.xl} />
    </p>
    <h1>Damn</h1>
    {error}
    <p>Something went wrong.</p>
    <p>Try again later, please!</p>
  {/await}
</AuthLayout>
