<script lang="ts">
  import { Link } from "svelte-navigator";

  import { paths } from "../constants";
  import { api } from "../stores";
  import AuthLayout from "../layouts/AuthLayout.svelte";
  import {
    APIStatus,
    Color,
    Gap,
    getErrorFor,
    IconName,
  } from "../types/components";
  import Icon from "../components/Icon.svelte";
  import Button from "../components/Button.svelte";

  const token = new URLSearchParams(window.location.search).get("token");

  const verifyToken = async () => {
    return await $api("/api/auth/onboard", {
      method: "POST",
      body: JSON.stringify({ token }),
    });
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
  }

  p + p {
    padding-top: var(--gap-md);
  }
</style>

<AuthLayout>
  {#await promise}
    <p>
      <Icon name={IconName.newspaper} size={Gap.xl} />
    </p>
    <h1>One sec...</h1>
    <p>Verifying your email...</p>
  {:then response}
    {#if response.status === APIStatus.ok}
      <p>
        <Icon name={IconName.thumbs_up} size={Gap.xl} />
      </p>
      <h1>All good!</h1>
      <p>Yey! You're good to go.</p>
      <p>
        <Link to={paths.LOGIN}>
          <Button color={Color.primary}>Log in!</Button>
        </Link>
      </p>
    {:else}
      <p>
        <Icon name={IconName.skull_crossbones} size={Gap.xl} />
      </p>
      <h1>Damn</h1>
      <p>{getErrorFor('token', response.body)}</p>
      <p>
        Have you tried our
        <Link to={paths.PASSWORD_RECOVERY}>password recovery</Link>? Or
        <Link to={paths.LOGIN}>log in</Link>
        if you've already got an account.
      </p>
    {/if}
  {:catch error}
    <p>
      <Icon name={IconName.skull_crossbones} size={Gap.xl} />
    </p>
    <h1>Damn</h1>
    {error}
    <p>Something went wrong.</p>
    <p>
      Have you tried our
      <Link to={paths.PASSWORD_RECOVERY}>password recovery</Link>? Or
      <Link to={paths.LOGIN}>log in</Link>
      if you've already got an account.
    </p>
  {/await}
</AuthLayout>
