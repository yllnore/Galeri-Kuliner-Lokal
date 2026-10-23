const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GaleriKuliner Smart Contract Test Suite", function () {
  let GaleriKuliner;
  let contract;
  let admin, curator, creator, user, unauthorized;

  const sampleWorkId = "soto-nusantara-01";
  const sampleURI = "ipfs://QmZ4tDuvesekSs4qM5ZBKpXiZGun7S2CYtEZRB3DYXkjGx";

  beforeEach(async function () {
    [admin, curator, creator, user, unauthorized] = await ethers.getSigners();
    GaleriKuliner = await ethers.getContractFactory("GaleriKuliner");
    contract = await GaleriKuliner.deploy(admin.address, curator.address);
    await contract.waitForDeployment();
  });

  describe("1. Inisialisasi & Deployment", function () {
    it("Harus memiliki nama dan simbol token yang benar", async function () {
      expect(await contract.name()).to.equal("Galeri Kuliner Nusantara");
      expect(await contract.symbol()).to.equal("GKN");
    });

    it("Harus menetapkan DEFAULT_ADMIN_ROLE dengan benar", async function () {
      const adminRole = await contract.DEFAULT_ADMIN_ROLE();
      expect(await contract.hasRole(adminRole, admin.address)).to.be.true;
    });

    it("Harus menetapkan CURATOR_ROLE kepada kurator awal", async function () {
      const curatorRole = await contract.CURATOR_ROLE();
      expect(await contract.hasRole(curatorRole, curator.address)).to.be.true;
    });

    it("Harus revert jika deployment menggunakan alamat admin nol", async function () {
      await expect(
        GaleriKuliner.deploy(ethers.ZeroAddress, curator.address)
      ).to.be.revertedWith("Admin tidak valid");
    });
  });

  describe("2. Hak Akses & Role Management", function () {
    it("Admin sah dapat menambahkan kurator baru", async function () {
      const curatorRole = await contract.CURATOR_ROLE();
      await contract.connect(admin).grantRole(curatorRole, user.address);
      expect(await contract.hasRole(curatorRole, user.address)).to.be.true;
    });

    it("Akun non-admin gagal menambahkan kurator baru (revert)", async function () {
      const curatorRole = await contract.CURATOR_ROLE();
      await expect(
        contract.connect(unauthorized).grantRole(curatorRole, user.address)
      ).to.be.reverted;
    });
  });

  describe("3. Fungsi Minting & Aturan Bisnis (P7)", function () {
    it("Kurator sah berhasil mencetak NFT kuliner baru", async function () {
      const tx = await contract.connect(curator).mintDish(creator.address, sampleWorkId, sampleURI);
      await tx.wait();

      expect(await contract.ownerOf(0)).to.equal(creator.address);
      expect(await contract.tokenURI(0)).to.equal(sampleURI);
      expect(await contract.isWorkRegistered(sampleWorkId)).to.be.true;
    });

    it("Bukan kurator gagal mencetak NFT (AccessControl revert)", async function () {
      await expect(
        contract.connect(unauthorized).mintDish(creator.address, sampleWorkId, sampleURI)
      ).to.be.reverted;
    });

    it("Mencegah duplikasi: Revert jika workId yang sama dicetak ulang", async function () {
      await contract.connect(curator).mintDish(creator.address, sampleWorkId, sampleURI);

      await expect(
        contract.connect(curator).mintDish(creator.address, sampleWorkId, "ipfs://QmLainnya")
      ).to.be.revertedWith("ID karya sudah pernah dicetak");
    });

    it("Revert jika parameter workId kosong", async function () {
      await expect(
        contract.connect(curator).mintDish(creator.address, "", sampleURI)
      ).to.be.revertedWith("Work ID tidak boleh kosong");
    });

    it("Revert jika parameter URI kosong", async function () {
      await expect(
        contract.connect(curator).mintDish(creator.address, "rendang-01", "")
      ).to.be.revertedWith("URI tidak boleh kosong");
    });

    it("Memancarkan event DishMinted dengan argumen yang benar saat mint", async function () {
      await expect(
        contract.connect(curator).mintDish(creator.address, sampleWorkId, sampleURI)
      )
        .to.emit(contract, "DishMinted")
        .withArgs(0, sampleWorkId, creator.address, curator.address, sampleURI);
    });
  });

  describe("4. Kepemilikan & Transfer", function () {
    beforeEach(async function () {
      await contract.connect(curator).mintDish(creator.address, sampleWorkId, sampleURI);
    });

    it("Pemilik sah dapat mentransfer NFT ke pengguna lain", async function () {
      await contract.connect(creator).transferFrom(creator.address, user.address, 0);
      expect(await contract.ownerOf(0)).to.equal(user.address);
    });

    it("Pihak yang tidak memiliki izin transfer gagal mentransfer token (revert)", async function () {
      await expect(
        contract.connect(unauthorized).transferFrom(creator.address, user.address, 0)
      ).to.be.reverted;
    });

    it("getWorkIdByTokenId mengembalikan workId yang tepat atau revert jika token belum ada", async function () {
      expect(await contract.getWorkIdByTokenId(0)).to.equal(sampleWorkId);
      await expect(contract.getWorkIdByTokenId(999)).to.be.reverted;
    });
  });
});