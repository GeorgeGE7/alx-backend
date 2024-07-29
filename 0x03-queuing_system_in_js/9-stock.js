#!/usr/bin/node
/**
 * Stock check
 */
import { promisify } from 'util';
import { createClient } from 'redis';
import express from 'express';

const redisClient = createClient();

redisClient.on('resError', (resError) => {
  console.log('Redis client not connected to the server:', resError.toString());
});

const listProducts = [
  {
    Id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  },
  {
    Id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  },
  {
    Id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  },
  {
    Id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

function transform(product) {
  const newOneMod = {};
  newOneMod.itemId = product.Id;
  newOneMod.itemName = product.name;
  newOneMod.price = product.price;
  newOneMod.initialAvailableQuantity = product.stock;
  return newOneMod;
}

function getItemById(id) {
  for (const prod of listProducts) {
    if (prod.Id === id) {
      return transform(prod);
    }
  }
  return {};
}

function getItems() {
  return listProducts.map(transform);
}

function reserveStockById(itemId, stock) {
  const SET = promisify(redisClient.SET).bind(redisClient);
  return SET(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById(itemId) {
  const Getclient = promisify(redisClient.GET).bind(redisClient);
  const stk = await Getclient(`item.${itemId}`);
  if (stk === null) return 0;
  return stk;
}

const app = express();

app.get('/list_products', (req, res) => {
  res.json(getItems());
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);
  if (Object.values(item).length > 0) {
    const stock = await getCurrentReservedStockById(itemId);
    item.currentQuantity = item.initialAvailableQuantity - stock;
    return res.json(item);
  }
  return res.json({ status: 'Product not found' });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);
  if (Object.values(item).length === 0) {
    return res.json({ status: 'Product not found' });
  }
  const stock = await getCurrentReservedStockById(itemId);
  if (stock >= item.initialAvailableQuantity) {
    return res.json({ status: 'Not enough stock available', itemId });
  }
  await reserveStockById(itemId, Number(stock) + 1);
  return res.json({ status: 'Reservation confirmed', itemId });
});

function clearRedisStock() {
  const SET = promisify(redisClient.SET).bind(redisClient);
  return Promise.all(listProducts.map((item) => SET(`item.${item.Id}`, 0)));
}

app.listen(1245, async () => {
  await clearRedisStock();
  console.log('API available on localhost via port 1245');
});
