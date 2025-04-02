/**
 * Converts a given number of bytes into a human-readable string format.
 *
 * @param {number} bytes - The number of bytes to format.
 * @param {number} [decimals=2] - The number of decimal places to include in the formatted output.
 * @returns {string} A string representing the formatted size in appropriate units (e.g., "KB", "MB").
 *
 * @example
 * formatBytes(1024); // "1.00 KB"
 * formatBytes(123456789, 3); // "117.738 MB"
 */
export const formatBytes = (bytes, decimals = 2) => {
  if (bytes == 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k)); //Determine which size gets
  const size = parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)); //Convert the bytes to the correspondent unit

  return size + " " + sizes[i]; // Concatenate the size with his unit
};

