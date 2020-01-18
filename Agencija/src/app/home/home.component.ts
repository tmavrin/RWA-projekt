import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  topOffers = [
    {
      title: 'Culture Tour',
      description:
        'Lorem ipsum dolor sit amet consectetur adipiscing elit, class nulla integer tristique pellentesque fringilla',
      image: 'assets/home/example_img1.png'
    },
    {
      title: 'Country Tour',
      description:
        'Lorem ipsum dolor sit amet consectetur adipiscing elit, class nulla integer tristique pellentesque fringilla',
      image: 'assets/home/example_img2.png'
    },
    {
      title: 'Nature Tour',
      description:
        'Lorem ipsum dolor sit amet consectetur adipiscing elit, class nulla integer tristique pellentesque fringilla',
      image: 'assets/home/example_img3.png'
    }
  ];

  constructor() {}

  ngOnInit() {}
}
