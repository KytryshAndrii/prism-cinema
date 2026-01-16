import { Box, styled, Typography } from "@mui/material";

export const ModalBox = styled(Box)(() => ({
  background: "rgba(15,15,15,0.96)",
  color: "#fff",
  padding: "2rem",
  borderRadius: "1rem",
  boxShadow: "0 0 30px rgba(0,0,0,0.8)",
  backdropFilter: "blur(12px)",
}));

export const ModalTitle = styled(Typography)(() => ({
  fontSize: "1.6rem",
  fontWeight: 700,
  marginBottom: "0.4rem",
}));

export const ModalSubtitle = styled(Typography)(() => ({
  fontSize: "0.95rem",
  color: "#aaa",
  marginBottom: "1rem",
}));

export const MoviesGrid = styled(Box)(() => ({
  display: "flex",
  flexWrap: "wrap",
  gap: "0.5rem",
}));

export const MovieChip = styled(Box)(() => ({
  padding: "0.35rem 0.8rem",
  background: "#1f1f1f",
  borderRadius: "1rem",
  fontSize: "0.85rem",
  cursor: "pointer",
  transition: "0.2s",
  border: "1px solid #2a2a2a",

  "&:hover": {
    background: "#2e2e2e",
    transform: "scale(1.05)",
  },
}));
