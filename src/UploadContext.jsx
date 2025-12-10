import { createContext, useState } from "react";

export const UploadContext = createContext();

export const UploadProvider = ({ children }) => {
  const [isUploaded, setIsUploaded] = useState(false);

  return (
    <UploadContext.Provider value={{ isUploaded, setIsUploaded }}>
      {children}
    </UploadContext.Provider>
  );
};
