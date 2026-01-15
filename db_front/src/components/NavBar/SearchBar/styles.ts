import { Box } from "@mui/material";
import { styled } from "@mui/system";


export const SearchWrapper = styled(Box)({
  position: "relative",
});

export const SearchInput = styled("input")({
  padding: "0.5rem 0.75rem",
  borderRadius: "1.25rem",
  border: "1px solid #ccc",
  background: "rgba(255, 255, 255, 0.08)",
  color: "white",
  fontSize: "0.875rem",
  width: "11.25rem",
});

export const SearchResults = styled("ul")({
  position: "absolute",
  top: "110%",
  left: 0,
  right: 0,
  background: "#121212",
  borderRadius: "0.5rem",
  maxHeight: "12.5rem",
  overflowY: "auto",
  zIndex: 10,
  listStyle: "none",
  padding: 0,
  margin: "0.25rem 0 0",
});

export const SearchResultItem = styled("li")({
  padding: "0.625rem 0.9375rem",
  cursor: "pointer",
  color: "white",
  "&:hover": {
    background: "#2d2d2d",
  },
});
