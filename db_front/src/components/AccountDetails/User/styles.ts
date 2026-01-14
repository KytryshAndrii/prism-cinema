import { Box, InputBase, Typography, Button } from "@mui/material";
import { styled } from "@mui/system";

export const ProfileWrapper = styled("form")({
  display: "flex",
  flexDirection: "column",
  gap: "1.5rem",
  padding: "3rem",
  maxWidth: "70vw",
  margin: "6rem auto",
  backgroundColor: "rgba(0, 0, 0, 0.9)",
  borderRadius: "1rem",
  color: "#fff",
});

export const ProfileTitle = styled(Typography)({
  fontSize: "2rem",
  fontWeight: "bold",
  textTransform: "uppercase",
  color: "#3FB7FF",
});

export const FieldLabel = styled(Typography)({
  fontSize: "1rem",
  fontWeight: "600",
  color: "#ddd",
});

export const FieldRow = styled(Box)({
  display: "flex",
  alignItems: "center",
  gap: "0.7rem",
});

export const StyledInput = styled(InputBase)({
  backgroundColor: "#dceeff",
  padding: "0.6rem 1rem",
  borderRadius: "0.4rem",
  width: "50%",
  fontWeight: "bold",
});

export const EditIconWrapper = styled(Box)({
  cursor: "pointer",
  display: "flex",
  alignItems: "center",
  color: "#aaa",
  "&:hover": {
    color: "#fff",
  },
});

export const ReadOnlyText = styled(Typography)({
  fontWeight: "bold",
  color: "#3FB7FF",
});

export const SaveButton = styled(Button)({
  display: "flex",
  alignSelf: "center",
  marginTop: "1.5rem",
  padding: "0.6rem",
  fontWeight: "bold",
  backgroundColor: "#3FB7FF",
  color: "#000",
  borderRadius: "8px",
  "&:hover": {
    backgroundColor: "#2ca0d8",
  },
});

export const NonEditableUserData = styled(Box)({
    display: "flex",
    flexDirection: "row",
    gap: "2rem"
})
