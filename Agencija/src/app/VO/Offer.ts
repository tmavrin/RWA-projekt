export class Offer {
  title: string;
  description: string;
  image: string;
  price: number;

  constructor(title, description, image, price) {
    this.title = title;
    this.description = description;
    this.image = image;
    this.price = price;
  }
}

export const DUMMY_OFFERS = [
  new Offer(
    'Culture Tour',
    'Lorem ipsum dolor sit amet consectetur adipiscing elit, class nulla integer tristique pellentesque fringilla,' +
        'nullam tellus feugiat aptent torquent nec. Eu velit ridiculus lacinia dignissim viverra magnis dapibus congue praesent.',
    'assets/images/example_img1.png',
    800
  ),
  new Offer(
    'Country Tour',
    'Lorem ipsum dolor sit amet consectetur adipiscing elit, class nulla integer tristique pellentesque fringilla,' +
        ' nullam tellus feugiat aptent torquent nec. Eu velit ridiculus lacinia dignissim viverra magnis dapibus congue praesent.',
    'assets/images/example_img2.png',
    50000
  ),
  new Offer(
    'Nature Tour',
    'Lorem ipsum dolor sit amet consectetur adipiscing elit, class nulla integer tristique pellentesque fringilla,' +
        ' nullam tellus feugiat aptent torquent nec. Eu velit ridiculus lacinia dignissim viverra magnis dapibus congue praesent.',
    'assets/images/example_img3.png',
    1
  )
];
