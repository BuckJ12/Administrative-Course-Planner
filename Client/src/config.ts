//export const apiUrl = process.env.APIURL;

export const apiUrl =
  process.env.NODE_ENV === 'production'
    ? 'https://heroic-tranquility-production.up.railway.app'
    : 'http://localhost:5000';

export const NodeMode = process.env.NODE_ENV;
