import express, {Request, Response} from 'express'
import dotenv from 'dotenv'
import path from 'path'

dotenv.config()
const app = express()
const port = process.env.PORT || 3000

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));


app.get('/', (req: Request, res: Response) => {
  res.send('Weed Mapper');
})

app.get('/map', (req: Request, res: Response) => {
  res.render('map', {
    title: '1',
    points: JSON.stringify([-33.712451, 150.311823])
  });
})
app.listen(port, () => {
  console.log(`[server] Server is running at http://localhost:${port}`)
})