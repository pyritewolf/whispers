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
  } from "../types/components";
  import Icon from "../components/Icon.svelte";

  const formData = {
    email: "",
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
    const response = await $api("/auth/password_recovery", {
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
  <h1>Password recovery</h1>
  {#if current_status === status.SUBMITTED}
    <p>
      <Icon name={NormalIcon.mail_bulk} size={Gap.xl} color={Color.secondary} />
    </p>
    <p>
      A mail will be arriving at your inbox shortly... it will hold great
      secrets.
    </p>
    <p>
      Those secrets are valid for 24hs so please go check your email, for real,
      tho.
    </p>
  {/if}
  {#if current_status !== status.SUBMITTED}
    <p>We'll need your e-mail to get started.</p>
    <form on:submit|preventDefault={handleSubmit}>
      <Input
        autofocus={true}
        label="E-mail"
        placeholder="coolstreamer@gmail.com"
        bind:value={formData.email}
        error={getErrorFor('email', formError)}
        name="email" />
      <Button
        color={Color.primary}
        disabled={current_status === status.LOADING}>
        Send recovery info
      </Button>
      <p>
        Remembered your password?
        <Link to={paths.SIGN_IN}>Sign in</Link>!
      </p>
    </form>
  {/if}
</AuthLayout>
