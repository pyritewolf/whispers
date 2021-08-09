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
    IconName,
    InputType,
  } from "../types/components";
  import Icon from "../components/Icon.svelte";

  const formData = {
    email: "",
    password: "",
    confirmPassword: "",
    username: "",
  };
  let formError = null;
  let formSubmitted = false;

  const handleSubmit = async () => {
    const response = await $api("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(formData),
    });
    if (response.status === APIStatus.error) return (formError = response.body);
    formError = null;
    formSubmitted = true;
  };
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
  <h1>Sign up</h1>
  {#if formSubmitted}
    <p>
      <Icon name={IconName.mail_bulk} size={Gap.xl} color={Color.secondary} />
    </p>
    <p>
      Cool! Now check your email like the good grown-up you are to complete the
      process.
    </p>
  {/if}
  <p>
    Already got an account?
    <Link to={paths.LOGIN}>Log in</Link>!
  </p>
  {#if !formSubmitted}
    <form on:submit|preventDefault={handleSubmit}>
      <Input
        autofocus={true}
        label="E-mail"
        placeholder="coolstreamer@gmail.com"
        bind:value={formData.email}
        error={getErrorFor('email', formError)}
        name="email" />
      <Input
        label="Username"
        placeholder="coolstreamer69"
        bind:value={formData.username}
        error={getErrorFor('username', formError)}
        name="username" />
      <Input
        label="Password"
        type={InputType.password}
        placeholder="safetaters69"
        bind:value={formData.password}
        error={getErrorFor('password', formError)}
        name="password" />
      <Input
        label="Repeat password"
        type={InputType.password}
        placeholder="safetaters69"
        bind:value={formData.confirmPassword}
        error={getErrorFor('confirm_password', formError)}
        name="confirm-password" />
      <Button color={Color.primary}>Get started!</Button>
    </form>
  {/if}
</AuthLayout>
