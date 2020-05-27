export default class PetApi {
  constructor() {
    this.token;
  }

  async getToken() {
    const resp = await axios.get("/api/get-token");
    // console.log(resp.data.token);
    this.token = resp.data.token;
    return this.token;
  }

  async getPets(type, location) {
    const resp = await axios.post("/api/get-pets", {
      token: this.token,
      type: type,
      location: location,
    });
    // console.log(resp.data);
    return resp.data.animals;
  }

  async getPet(id) {
    const resp = await axios.post("/api/get-pet", {
      token: this.token,
      id: id,
    });
    // console.log(resp.data);
    return resp.data;
  }
}
