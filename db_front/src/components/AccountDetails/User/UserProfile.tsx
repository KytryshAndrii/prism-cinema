import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { useSelector } from "react-redux";
import EditIcon from "@mui/icons-material/Edit";
import type { AppState } from "../../../store/store";
import { EditIconWrapper, FieldLabel, FieldRow, NonEditableUserData, ProfileTitle, ProfileWrapper, ReadOnlyText, SaveButton, StyledInput } from "./styles";
import type { tFormValues } from "./types";

const UserProfile: React.FC = () => {
  const user = useSelector((state: AppState) => state.user);

  const [isEditingLogin, setIsEditingLogin] = useState(false);
  const [isEditingEmail, setIsEditingEmail] = useState(false);
  const [isEditingPassword, setIsEditingPassword] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<tFormValues>({
    defaultValues: {
      login: user.login ?? "",
      email: user.email ?? "",
      password: "",
      confirmPassword: "",
    },
  });

  const onSubmit = (data: tFormValues) => {
    console.log("Form Data:", data);
    // Integracja z authApi → np. authApi.updateUserProfile(data)
  };

  const password = watch("password");

  return (
    <ProfileWrapper onSubmit={handleSubmit(onSubmit)}>
      <ProfileTitle>PROFILE</ProfileTitle>

      {/* Username */}
      <FieldLabel>Username</FieldLabel>
      <FieldRow>
        <StyledInput
          disabled={!isEditingLogin}
          {...register("login", { required: true })}
        />
        <EditIconWrapper onClick={() => setIsEditingLogin(!isEditingLogin)}>
          <EditIcon />
        </EditIconWrapper>
      </FieldRow>

      {/* Password */}
      <FieldLabel>Password</FieldLabel>
      <FieldRow>
        <StyledInput
          type="password"
          disabled={!isEditingPassword}
          {...register("password", {
            required: isEditingPassword,
            minLength: 6,
          })}
        />
        <EditIconWrapper onClick={() => setIsEditingPassword(!isEditingPassword)}>
          <EditIcon />
        </EditIconWrapper>
      </FieldRow>

      {isEditingPassword && (
        <>
          <FieldLabel>Confirm Password</FieldLabel>
          <FieldRow>
            <StyledInput
              type="password"
              {...register("confirmPassword", {
                validate: (value) =>
                  value === password || "Passwords do not match",
              })}
            />
          </FieldRow>
        </>
      )}

      {/* Email */}
      <FieldLabel>Email address</FieldLabel>
      <FieldRow>
        <StyledInput
          type="email"
          disabled={!isEditingEmail}
          {...register("email", { required: true })}
        />
        <EditIconWrapper onClick={() => setIsEditingEmail(!isEditingEmail)}>
          <EditIcon />
        </EditIconWrapper>
      </FieldRow>

      {/* Birthdate (read-only) */}
      <NonEditableUserData>
        <FieldLabel>Date of Birth:</FieldLabel>
        <ReadOnlyText>1990-12-12</ReadOnlyText> {/* TODO: dynamicznie z backendu */}
      </NonEditableUserData>
      {/* Region (read-only) */}
      <NonEditableUserData>
        <FieldLabel>Region:</FieldLabel>
        <ReadOnlyText>Poland</ReadOnlyText> {/* TODO: dynamicznie z backendu */}
      </NonEditableUserData>
      <SaveButton type="submit">Save changes</SaveButton>
    </ProfileWrapper>
  );
};

export default UserProfile;
