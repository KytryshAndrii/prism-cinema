export const getRegionFromLocale = (): string => {
  try {
    const locale = Intl.DateTimeFormat().resolvedOptions().locale;
    const countryCode = locale.split("-")[1] || " ";
    return countryCode.toUpperCase();
  } catch {
    return "";
  }
};