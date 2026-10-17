import axios from "axios"

export const postWarehouseLocation = data =>
  axios.post("http://127.0.0.1:5000/getWarehouseLocation", data).then(response => response.data)
