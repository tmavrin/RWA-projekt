export class Offer {
  description: string;
  id: string;
  image: any;
  isTop: number;
  pdf: any;
  price: number;
  title: string;

  constructor(title, description, price) {
    this.title = title;
    this.description = description;
    this.price = price;
  }
}
