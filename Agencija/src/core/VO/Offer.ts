export class Offer {
  description: string;
  id: string;
  image: string;
  isTop: number;
  pdf: string;
  price: number;
  title: string;

  constructor(title, description, price) {
    this.title = title;
    this.description = description;
    this.price = price;
  }
}
