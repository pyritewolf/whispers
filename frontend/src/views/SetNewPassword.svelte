<script lang="ts">
  import { Link } from "svelte-navigator";
  import { paths } from "../constants";
  import { api } from "../stores";
  import AuthLayout from "../layouts/AuthLayout.svelte";
  import Input from "../components/Input.svelte";
  import Button from "../components/Button.svelte";
  import {
    APIStatus,
    Color,
    Gap,
    getErrorFor,
    NormalIcon,
    InputType,
  } from "../types/components";
  import Icon from "../components/Icon.svelte";

  const token = new URLSearchParams(window.location.search).get("token");

  const formData = {
    password: "",
    confirmPassword: "",
    token,
  };

  const status = {
    STARTED: "STARTED",
    LOADING: "LOADING",
    SUBMITTED: "SUBMITTED",
  };
  let formError = null;
  let current_status = status.STARTED;

  const handleSubmit = async () => {
    current_status = status.LOADING;
    const response = await $api("/auth/new_password", {
      method: "POST",
      body: JSON.stringify(formData),
    });
    if (response.status === APIStatus.error) return (formError = response.body);
    formError = null;
    current_status = status.SUBMITTED;
  };
</script>

<style>
  h1 {
    text-align: center;
  }

  p {
    text-align: center;
    padding-top: var(--gap-md);
  }

  h1 + p {
    padding-bottom: var(--gap-md);
  }
</style>

<AuthLayout>
  {#if current_status === status.SUBMITTED}
    <p>
      <Icon name={NormalIcon.thumbs_up} size={Gap.xl} />
    </p>
    <h1>Hooray!</h1>
    <p>Your password was changed. Time to get back in!</p>
    <p>
      <Link to={paths.SIGN_IN}>
        <Button color={Color.primary}>Sign in</Button>
      </Link>
    </p>
  {/if}
  {#if current_status !== status.SUBMITTED}
    <h1>Password recovery</h1>
    <p>
      Let's see that new password of yours. Make it... memorable and mysterious.
    </p>
    <form on:submit|preventDefault={handleSubmit}>
      <Input
        label="Password"
        placeholder="safepw69"
        type={InputType.password}
        bind:value={formData.password}
        error={getErrorFor('password', formError)}
        name="password" />
      <Input
        label="Repeat your password"
        placeholder="safepw69"
        type={InputType.password}
        bind:value={formData.confirmPassword}
        error={getErrorFor('confirm_password', formError)}
        name="confirm_password" />
      <Button
        color={Color.primary}
        disabled={current_status === status.LOADING}>
        Save password
      </Button>
      <p>
        Remembered your old password?
        <Link to={paths.SIGN_IN}>Sign in</Link>!
      </p>
    </form>
  {/if}
</AuthLayout>
