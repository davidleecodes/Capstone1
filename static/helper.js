export default class PetApi {
  constructor() {
    this.token;
  }

  async getPets(type, location, page) {
    const resp = await axios.post("/api/get-pets", {
      // token: this.token,
      type: type,
      location: location,
      page: page,
    });
    console.log(resp.data);

    return resp.data;
  }

  async getPet(id) {
    const resp = await axios.post("/api/get-pet", {
      token: this.token,
      id: id,
    });
    // console.log(resp.data);
    return resp.data;
  }

  async getTypes() {
    const resp = await axios.post("/api/get-types", {
      token: this.token,
    });
    // console.log(resp.data);
    return resp.data;
  }
}
