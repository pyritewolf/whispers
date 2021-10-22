<script lang="ts">
  import { Link, navigate } from "svelte-navigator";
  import { paths } from "../constants";
  import { api } from "../stores";
  import AuthLayout from "../layouts/AuthLayout.svelte";
  import Input from "../components/Input.svelte";
  import Button from "../components/Button.svelte";
  import { user } from "../stores";
  import {
    APIStatus,
    Color,
    getErrorFor,
    InputType,
  } from "../types/components";

  const formData = {
    userIdentifier: "",
    password: "",
  };
  let formError = null;

  const handleSubmit = async () => {
    const params = new URLSearchParams();
    params.append("username", formData.userIdentifier);
    params.append("password", formData.password);
    const response = await $api("/auth/signin", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params,
    });
    if (response.status === APIStatus.error) return (formError = response.body);
    formError = null;
    user.set(response.body);
    navigate(paths.HOME);
  };
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
  <h1>Sign in</h1>
  <p>
    Having trouble?
    <Link to={paths.PASSWORD_RECOVERY}>Reset your password</Link>!
  </p>
  <form on:submit|preventDefault={handleSubmit}>
    <Input
      autofocus={true}
      label="E-mail or username"
      placeholder="coolstreamer@gmail.com"
      bind:value={formData.userIdentifier}
      name="user_identifier" />
    <Input
      label="Password"
      type={InputType.password}
      placeholder="safetaters69"
      bind:value={formData.password}
      error={getErrorFor('auth', formError)}
      name="password" />
    <Button color={Color.primary}>Sign in!</Button>
  </form>
</AuthLayout>
